import logging
import os
from errors import ERROR_DATA_DIRECTORY_NOT_SET, exit_everything

_paths: 'dict[str, str]' = dict()

_DATA_DIRECTORY_ENV_KEY = 'DATA_DIR'
_DATABASE_PATH_KEY = 'db'
_MEDIA_DIRECTORY_KEY = 'media'
_THUMBNAILS_DIRECTORY_KEY = 'thumbnails'


def _try_make_dir(path: str):
	try:
		os.makedirs(path)
		logging.info(f'Created directory {path}')
	except FileExistsError:
		logging.debug(f'Directory {path} existed')
	except OSError as e:
		logging.error(f'Error while making directory {path}', exc_info=e)


def initialize_paths():
	"""Initialize all paths used by everything"""
	if os.getenv(_DATA_DIRECTORY_ENV_KEY) is None:
		exit_everything(ERROR_DATA_DIRECTORY_NOT_SET, f'{_DATA_DIRECTORY_ENV_KEY} env var not set')
	
	data_dir = os.getenv(_DATA_DIRECTORY_ENV_KEY)
	_paths[_DATABASE_PATH_KEY] = os.path.join(data_dir, 'everything.db')
	_paths[_MEDIA_DIRECTORY_KEY] = os.path.join(data_dir, 'media')
	_paths[_THUMBNAILS_DIRECTORY_KEY] = os.path.join(_paths[_MEDIA_DIRECTORY_KEY], '.thumbnails')

	# Create directories
	_try_make_dir(_paths[_MEDIA_DIRECTORY_KEY])
	_try_make_dir(_paths[_THUMBNAILS_DIRECTORY_KEY])


def get_database_path():
	"""Returns the path to the database file"""
	return _paths[_DATABASE_PATH_KEY]


def get_media_directory():
	"""Returns the path to the media directory"""
	return _paths[_MEDIA_DIRECTORY_KEY]


def get_thumbnails_directory():
	"""Returns the path to the thumbnails directory"""
	return _paths[_THUMBNAILS_DIRECTORY_KEY]

