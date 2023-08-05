import os.path
import egnyte
import re
import time

from .logger import flogger
from .bytesize import bytes_scaled

elog = flogger(label='EGNYTE')


## init

_updates = False

config = egnyte.configuration.load()

if "api_key" not in config:
	config["api_key"] = "zxuez95f5utrrf7v2ukyex6y"
	_updates = True

if "client_id" not in config:
	config["client_id"] = "zxuez95f5utrrf7v2ukyex6y"
	_updates = True

if "domain" not in config:
	config["domain"] = "camsys"
	_updates = True

if "time_between_requests" not in config:
	config["time_between_requests"] = 1
	_updates = True

if _updates:
	egnyte.configuration.save(config)


client = egnyte.EgnyteClient(config)


def _folder_to_path(f):
	if isinstance(f,egnyte.resources.Folder):
		return f.path
	if isinstance(f,egnyte.resources.File):
		return f.path
	return f

def pth(*arg):
	return "/".join(_folder_to_path(f) for f in arg).replace('//','/').replace('\\','/')


def _load_obj(obj, retries=10, interval=1):
	for i in range(retries):
		try:
			obj._get()
		except egnyte.exc.NotAuthorized:
			elog(f'Try {i} NotAuthorized:'+str(obj).replace("{","[").replace("}","]"))
			time.sleep(interval)
		else:
			break


def create_folder(folder_path, retries=10, interval=1):
	"""
	Create a new folder within Egnyte.

	:param folder_path:
	:return: egnyte.resources.Folder
	"""
	for i in range(retries):
		try:
			folder = client.folder(pth(folder_path)).create(ignore_if_exists=True)
		except egnyte.exc.NotAuthorized:
			elog(f'Create Folder Attempt {i} NotAuthorized:'+str(folder_path).replace("{","[").replace("}","]"))
			time.sleep(interval)
		else:
			break
	return folder

def create_subfolder(folder, subfoldername):
	f = client.folder(pth(folder,subfoldername)).create(ignore_if_exists=True)
	return f

def upload_file(local_file, egnyte_path):
	basename = os.path.basename(local_file)
	file_obj = client.file( pth(egnyte_path,basename) )
	with open(local_file, "rb") as fp:
		file_obj.upload(fp)

def upload_file_gz(local_file, egnyte_path, progress_callbacks=None):
	if progress_callbacks is None:
		progress_callbacks = ProgressCallbacks()
	import gzip, io, shutil
	basename = os.path.basename(local_file)+'.gz'
	file_obj = client.file(pth(egnyte_path, basename))
	buffer = io.BytesIO()
	with open(local_file, 'rb') as f_in:
		with gzip.open(buffer, 'wb') as buffer_out:
			shutil.copyfileobj(f_in, buffer_out)
	progress_callbacks.upload_start(local_file, file_obj, buffer.tell())
	file_obj.upload(buffer)
	progress_callbacks.upload_finish(file_obj)


def upload_dict_json(dictionary, filename, egnyte_path, progress_callbacks=None, retries=10, interval=1):
	"""

	Parameters
	----------
	dictionary : dict
		The dictionary to convert to json and upload to egnyte
	filename : str
		A filename for the file that will be created in egnyte
	egnyte_path : str
		The (existing) folder in egnyte where the file will be created
	progress_callbacks

	"""
	if progress_callbacks is None:
		progress_callbacks = ProgressCallbacks()
	import json, io
	basename = os.path.basename(filename)
	if basename[-5:] != '.json':
		basename += '.json'
	file_obj = client.file(pth(egnyte_path, basename))
	buffer = io.BytesIO(json.dumps(dictionary).encode('UTF-8'))
	progress_callbacks.upload_start("dictionary", file_obj, buffer.tell())
	for i in range(retries):
		try:
			file_obj.upload(buffer)
		except egnyte.exc.NotAuthorized:
			elog('upload NotAuthorized: '+str(file_obj).replace('{','[').replace('}',']'))
			time.sleep(interval)
		else:
			break
	progress_callbacks.upload_finish(file_obj)



def download_file(egnyte_file, local_path, overwrite=False, mkdir=True, progress_callbacks=None, retries=10, interval=1):
	if not os.path.exists(local_path) and mkdir:
		os.makedirs(local_path)
	success = False
	for i in range(retries):
		try:
			client.bulk_download([egnyte_file], local_path, overwrite=overwrite, progress_callbacks=progress_callbacks)
		except egnyte.exc.NotAuthorized:
			elog('download NotAuthorized: ' + str(egnyte_file).replace('{', '[').replace('}', ']'))
			time.sleep(interval)
		except egnyte.exc.NotFound:
			raise FileNotFoundError(f'egnyte:{egnyte_file}')
		else:
			success = True
			break
	if not success:
		raise egnyte.exc.NotAuthorized(f'after {retries} tries')


def download_file_gz(egnyte_file, local_path, overwrite=False, mkdir=True, progress_callbacks=None, retries=10, interval=1):
	if progress_callbacks is None:
		progress_callbacks = ProgressCallbacks()
	if not os.path.exists(local_path) and mkdir:
		os.makedirs(local_path)
	import gzip, io, shutil
	if isinstance(egnyte_file, str) and egnyte_file[-3:] != '.gz':
		egnyte_file = egnyte_file+'.gz'
	basename = os.path.basename(egnyte_file)[:-3]
	if not overwrite and os.path.exists(os.path.join(local_path, basename)):
		raise FileExistsError(os.path.join(local_path, basename))
	try:
		file_obj = client.file(pth(egnyte_file))
		buffer = io.BytesIO()
		try:
			progress_callbacks.download_start(local_path, file_obj, file_obj.size)
		except egnyte.exc.NotAuthorized:
			progress_callbacks.download_start(local_path, file_obj, -1)
		for i in range(retries):
			try:
				file_obj.download().write_to(buffer, progress_callbacks.download_progress)
			except egnyte.exc.NotAuthorized:
				elog('download NotAuthorized: '+str(file_obj).replace('{','[').replace('}',']'))
				time.sleep(interval)
			else:
				break
		buffer.seek(0)
		with gzip.open(buffer, 'rb') as buffer_in:
			with open(os.path.join(local_path, basename), 'wb') as f_out:
				shutil.copyfileobj(buffer_in, f_out)
		progress_callbacks.download_finish(file_obj)
	except egnyte.exc.NotFound:
		raise FileNotFoundError(f'egnyte:{egnyte_file}')


def download_dict_json(egnyte_file, progress_callbacks=None, retries=10, interval=1):
	"""

	Parameters
	----------
	egnyte_file : str
		The location in egnyte for the json file to be loaded.
	progress_callbacks

	Returns
	-------
	dict
	"""
	if progress_callbacks is None:
		progress_callbacks = ProgressCallbacks()
	import json, io
	if isinstance(egnyte_file, str) and egnyte_file[-5:] != '.json':
		egnyte_file = egnyte_file+'.json'
	try:
		file_obj = client.file(pth(egnyte_file))
		buffer = io.BytesIO()
		_load_obj(file_obj)
		try:
			progress_callbacks.download_start('dictionary', file_obj, file_obj.size)
		except egnyte.exc.NotAuthorized:
			progress_callbacks.download_start('dictionary', file_obj, -1)
		for i in range(retries):
			try:
				file_obj.download().write_to(buffer, progress_callbacks.download_progress)
			except egnyte.exc.NotAuthorized:
				elog('download NotAuthorized: '+str(file_obj).replace('{','[').replace('}',']'))
				time.sleep(interval)
			else:
				break
		buffer.seek(0)
		result = json.loads(buffer.getvalue().decode('UTF-8'))
		progress_callbacks.download_finish(file_obj)
		return result
	except egnyte.exc.NotFound:
		raise FileNotFoundError(f'egnyte:{egnyte_file}')


# def batch_upload_file(local_files, egnyte_path):
# 	for local_file in local_files:
# 		upload_file(local_file, egnyte_path)
#
# def batch_upload_directory(local_dir, egnyte_path):
# 	for root, dirs, files in os.walk(local_dir):
# 		fo = create_folder( pth(egnyte_path,os.path.relpath(root, local_dir)) )
# 		batch_upload_file((os.path.join(root, fi) for fi in files), fo)


def next_result_folder(egnyte_path, descrip, local_dir=None):
	c = re.compile('^([0-9]+)\\s.+')
	seen_max = 0
	eg_folder = client.folder(pth(egnyte_path))
	_load_obj(eg_folder)
	for fo in eg_folder.folders:
		match = c.match(fo.name)
		if match:
			seen_max = max(seen_max, int(match.group(1)))
	result_folder = create_subfolder(eg_folder, subfoldername="{0:04d} {1}".format(seen_max+1, descrip))
	bulk_upload(local_dir, result_folder, log=True)
	return result_folder



class ProgressCallbacks(egnyte.client.ProgressCallbacks):
	"""
	This object is used for bulk transfers (uploads and downloads)
	Inherit this and add override any of the callabcks you'd like to handle.
	"""

	def getting_info(self, cloud_path):
		"""Getting information about an object. Called for directories and unknown paths."""
		elog("getting info on {}".format(cloud_path))

	def got_info(self, cloud_obj):
		"""Got information about an object."""

	def creating_directory(self, cloud_folder):
		"""Creating a directory."""
		elog("creating directory {}".format(cloud_folder))

	def download_start(self, local_path, cloud_file, size):
		"""Starting to download a file."""
		elog("downloading {1} ({2})".format(local_path, cloud_file.path, bytes_scaled(size)))

	def download_progress(self, cloud_file, size, downloaded):
		"""Some progress in file download."""

	def download_finish(self, cloud_file):
		"""Finished downloading a file."""

	def upload_start(self, local_path, cloud_file, size):
		"""Starting to upload a file."""
		elog("uploading {1} ({2})".format(local_path, cloud_file.path, bytes_scaled(size)))

	def upload_progress(self, cloud_file, size, uploaded):
		"""Some progress in file upload."""

	def upload_finish(self, cloud_file):
		"""Finished uploading a file."""

	def finished(self):
		"""Called after all operations."""
		elog("finished")

	def skipped(self, cloud_obj, reason):
		"""Object has been skipped because of 'reason'"""
		elog("skipped {} ({})".format(cloud_obj, reason))




def bulk_upload( local_dir, egnyte_path, log=True ):
	if isinstance(local_dir, str):
		client.bulk_upload([local_dir], egnyte_path, ProgressCallbacks() if log else None)
	else:
		client.bulk_upload(local_dir, egnyte_path, ProgressCallbacks() if log else None)

def bulk_download( egnyte_path, local_dir, log=True, overwrite=False ):
	if isinstance(egnyte_path, str):
		client.bulk_download([egnyte_path], local_dir, overwrite=overwrite, progress_callbacks=ProgressCallbacks() if log else None)
	else:
		client.bulk_download(egnyte_path, local_dir, overwrite=overwrite, progress_callbacks=ProgressCallbacks() if log else None)





def get_access_token():
	import requests, getpass
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	data = [
		('grant_type', 'password'),
		('username', getpass.getpass("Username (not email, just name): ")),
		('password', getpass.getpass("Password: ")),
		('client_id', 'zxuez95f5utrrf7v2ukyex6y'),
	]
	response = requests.post('https://camsys.egnyte.com/puboauth/token', headers=headers, data=data)
	response_json = response.json()
	if 'access_token' in response_json:
		client.config['access_token'] = response_json['access_token']
	egnyte.configuration.save(client.config)
