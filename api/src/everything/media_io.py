import os
import sys
import subprocess
from datetime import datetime
from everything.db import Media


image_extensions = ['.jpg', '.png', '.jpeg']
video_extensions = ['.mp4', '.mov']
allowed_extensions = image_extensions + video_extensions


def _format_date_to_touch(datetime: datetime) -> str:
	"""Returns datettime in Date Modified format for touch command

	Format: YYYYMMDDhhmm.SS

	See: https://www.thegeekstuff.com/2012/11/linux-touch-command/
	"""
	return datetime.strftime('%Y%m%d%H%M.%S')


def _modify_date_unix_command(media: Media) -> str:
	"""Returns command to modify Date Modified for macOS and Linux

	Command: `touch -a -m -t YYYYMMDDhhmm.SS filename`

	See: https://smallbusiness.chron.com/change-file-date-mac-finder-46835.html
	"""
	return f'touch -a -m -t {_format_date_to_touch(media.date)} {media.filepath}'


def write_date_to_media(media: Media):
	command = None

	if sys.platform in ['darwin', 'linux', 'linux2']:
		command = _modify_date_unix_command(media)
	else:
		raise ValueError(f'Running on unsupported OS {sys.platform}')

	# Run command
	subprocess.run(command, shell=True, check=True)


def get_extension(filepath: str):
	"""Returns the extension of a filepath
	
	Parameters:
		filepath (str): The filepath to retreive the extension of
	"""
	_, ext = os.path.splitext(filepath)
	return ext


def is_image(filepath: str) -> bool:
	"""Returns whether a filepath is an image"""
	ext = get_extension(filepath)
	return ext.lower() in image_extensions


def is_media_file(filepath: str) -> bool:
	"""Returns whether this file can be stored as Media
	
	Parameters:
		filepath (str): Full filepath of file
	"""
	ext = get_extension(filepath)
	return ext.lower() in allowed_extensions


def mime_from_ext(filepath: str):
	"""TODO"""
	ext = get_extension(filepath)
	return {
		'.jpg': 'image/jpeg',
		'.jpeg': 'image/jpeg',
		'.png': 'image/png',
		'.mp4': 'video/mp4',
		'.mov': 'application/octet-stream'
	}[ext.lower()]
