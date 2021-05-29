import logging
import os
import typing
from datetime import datetime
from everything.db import Media
from everything.paths import get_media_directory
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


image_extensions = ['.jpg', '.png', '.jpeg']
video_extensions = ['.mp4', '.mov']
allowed_extensions = image_extensions + video_extensions


def get_extension(filepath: str):
	"""Returns the extension of a filepath
	
	Parameters:
		filepath (str): The filepath to retreive the extension of
	"""
	_, ext = os.path.splitext(filepath)
	return ext


def mime_from_ext(filepath: str):
	ext = get_extension(filepath)
	return {
		'.jpg': 'image/jpeg',
		'.jpeg': 'image/jpeg',
		'.png': 'image/png',
		'.mp4': 'video/mp4',
		'.mov': 'application/octet-stream'
	}[ext.lower()]


def is_image(filepath: str) -> bool:
	"""Returns whether a filepath is an image"""
	ext = get_extension(filepath)
	return ext.lower() in image_extensions


def _read_date(filepath: str) -> datetime:
	"""Read Modification Date from filepath"""
	epoch_time = os.path.getmtime(filepath)
	return datetime.fromtimestamp(epoch_time)


def _read_location(filepath: str) -> typing.Optional[str]:
	"""Returns a POINT(lat, long) string if the media at the filepath contains a location.

	Note: Currently only images are supported for location reading. If the passed filepath
		points to a video, `None` will be returned.

	Parameters:
		filepath (str): The filepath of the media

	Returns: `None` in the case that the media doesn't have a location.
	"""
	if not is_image(filepath):
		return None

	exif: 'dict[str, Any]' = Image.open(filepath)._getexif()
	# No EXIF tags
	if exif is None:
		return None

	exif = { TAGS.get(key, key): v for (key, v) in exif.items() }

	# No GPS info in EXIF tags
	if not 'GPSInfo' in exif:
		return None

	exif = { GPSTAGS.get(key, key): v for (key, v) in exif['GPSInfo'].items() }

	# Convert from DMS to decimal
	for key in ['Latitude', 'Longitude']:
		if f'GPS{key}' in exif and f'GPS{key}Ref' in exif:
			deg, min, sec = [float(i) for i in exif[f'GPS{key}']]
			ref = exif[f'GPS{key}Ref']
			exif[key] = round(deg + min / 60 + sec / 3600, 5) * (-1 if ref in ['S','W'] else 1)

	if 'Latitude' in exif and 'Longitude' in exif:
		lat = exif['Latitude']
		lon = exif['Longitude']
		return f'POINT({lat} {lon})'

	return None


def is_media_file(filepath: str) -> bool:
	"""Returns whether this file can be stored as Media
	
	Parameters:
		filepath (str): Full filepath of file
	"""
	ext = get_extension(filepath)
	return ext.lower() in allowed_extensions


def scan() -> typing.List[Media]:
	"""Scan all items from disk to be stored in the database
	
	Returns: the list of media found in this directory
	"""
	retval = []
	logging.info(f'Scanning directory {get_media_directory()}')

	for root, _, files in os.walk(get_media_directory()):
		for filename in files:
			filepath = os.path.join(root, filename)
			if not is_media_file(filepath):
				continue
				
			media_date = _read_date(filepath)
			media_location = _read_location(filepath)
			media_item = Media(filepath=filepath, date=media_date, location=media_location)

			if not media_location is None:
				logging.debug(f'Media with location {filepath} -> {media_location}')

			retval.append(media_item)
	
	logging.info(f'Scanned {len(retval)} media items')
	return retval
