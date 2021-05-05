import logging
import os
import typing
from datetime import datetime
from db import Media
from paths import get_media_directory, get_thumbnails_directory


image_extensions = ['.jpg', '.png', '.jpeg']
video_extensions = ['.mp4', '.mov']
allowed_extensions = image_extensions + video_extensions


def mime_from_ext(filepath):
	_, ext = os.path.splitext(filepath)
	return {
		'.jpg': 'image/jpeg',
		'.jpeg': 'image/jpeg',
		'.png': 'image/png',
		'.mp4': 'video/mp4',
		'.mov': 'application/octet-stream'
	}[ext.lower()]


def is_image(filepath: str) -> bool:
	"""Returns whether a filepath is an image"""
	_, ext = os.path.splitext(filepath)
	return ext.lower() in image_extensions


def _read_date(filepath: str) -> datetime:
	"""Read Modification Date from filepath"""
	epoch_time = os.path.getmtime(filepath)
	return datetime.fromtimestamp(epoch_time)


def _is_media_file(filepath: str) -> bool:
	"""Returns whether this file can be stored as media."""
	_, ext = os.path.splitext(filepath)
	return ext.lower() in allowed_extensions


def scan() -> typing.List[Media]:
	"""Scan all items from disk to be stored in the database
	
	Returns: the list of media found in this directory
	"""
	retval = []
	logging.info(f'Scanning directory {get_media_directory()}')

	for root, dirs, files in os.walk(get_media_directory()):
		# Ignore thumbnail directory
		dirs[:] = [d for d in dirs if not d == get_thumbnails_directory()]

		for filename in files:
			filepath = os.path.join(root, filename)
			if not _is_media_file(filepath):
				continue
				
			media_date = _read_date(filepath)
			media_item = Media(filepath=filepath, date=media_date)

			retval.append(media_item)
	
	return retval
