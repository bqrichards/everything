import os
import string
import logging
import random
from everything.errors import ERROR_DATA_DIRECTORY_NOT_SET, ERROR_FRONTEND_NOT_SET, exit_everything

_paths: 'dict[str, str]' = dict()

_DATA_DIRECTORY_ENV_KEY = 'DATA_DIR'
_FRONTEND_URL_ENV_KEY = 'FRONTEND_URL'

_DATA_DIRECTORY_KEY = 'data'
_DATABASE_PATH_KEY = 'db'
_MEDIA_DIRECTORY_KEY = 'media'
_THUMBNAILS_DIRECTORY_KEY = 'thumbnails'


def _generate_random_string(length: int):
	"""Returns a random alphanumeric string
	
	Parameters:
		length (int): the length of the generated string
	"""
	all_chars = string.ascii_letters + string.digits
	return ''.join(random.choices(all_chars, k=length))


def _check_env():
	""" Ensure all enviroment variables are set. Crashes if not. """
	if os.getenv(_DATA_DIRECTORY_ENV_KEY) is None:
		exit_everything(ERROR_DATA_DIRECTORY_NOT_SET, f'{_DATA_DIRECTORY_ENV_KEY} env var not set')
	
	if os.getenv(_FRONTEND_URL_ENV_KEY) is None:
		exit_everything(ERROR_FRONTEND_NOT_SET, f'{_FRONTEND_URL_ENV_KEY} env var not set')


def _try_make_dir(path: str):
	try:
		os.makedirs(path)
		logging.info(f'Created directory {path}')
	except FileExistsError:
		logging.info(f'Directory {path} existed')
	except OSError as e:
		logging.error(f'Error while making directory {path}', exc_info=e)


def _log_paths():
	logging.info('Paths:')
	logging.info(f'Data Directory: {_paths[_DATA_DIRECTORY_KEY]}')
	logging.info(f'Database File: {_paths[_DATABASE_PATH_KEY]}')
	logging.info(f'Media Directory: {_paths[_MEDIA_DIRECTORY_KEY]}')
	logging.info(f'Thumbnails Directory: {_paths[_THUMBNAILS_DIRECTORY_KEY]}')


def initialize_paths():
	"""Initialize all paths used by everything"""
	_check_env()
	
	data_dir = os.getenv(_DATA_DIRECTORY_ENV_KEY)
	_paths[_DATA_DIRECTORY_KEY] = data_dir
	_paths[_DATABASE_PATH_KEY] = os.path.join(data_dir, 'everything.db')
	_paths[_MEDIA_DIRECTORY_KEY] = os.path.join(data_dir, 'media')
	_paths[_THUMBNAILS_DIRECTORY_KEY] = os.path.join(data_dir, '.thumbnails')

	# Create directories
	_try_make_dir(_paths[_MEDIA_DIRECTORY_KEY])
	_try_make_dir(_paths[_THUMBNAILS_DIRECTORY_KEY])

	_log_paths()
	os.remove(get_database_path())


def get_data_path():
	"""Returns the path to the data folder"""
	return _paths[_DATA_DIRECTORY_KEY]


def get_database_path():
	"""Returns the path to the database file"""
	return _paths[_DATABASE_PATH_KEY]


def get_media_directory():
	"""Returns the path to the media directory"""
	return _paths[_MEDIA_DIRECTORY_KEY]


def get_thumbnails_directory():
	"""Returns the path to the thumbnails directory"""
	return _paths[_THUMBNAILS_DIRECTORY_KEY]


def generate_random_media_filepath(extension: str):
	"""Returns a new random path for a media file
	
	Parameters:
		extension (str): extension of file (including .) Example: `.png`
	"""
	filename = f'{_generate_random_string(30)}{extension}'
	return os.path.join(get_media_directory(), filename)
