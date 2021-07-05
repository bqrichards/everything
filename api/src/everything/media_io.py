import os
import sys
import subprocess
from PIL import Image
from datetime import datetime
from typing import Any, Optional
from PIL.ExifTags import GPSTAGS, TAGS
from everything.db import Media
from imagehash import dhash


image_extensions = ['.jpg', '.png', '.jpeg']
video_extensions = ['.mp4', '.mov']
allowed_extensions = image_extensions + video_extensions


def _compute_video_hash() -> str:
	"""TODO"""
	return 'video'


def _compute_image_fingerprint(image_data: Image) -> str:
	"""Calculates a fingerprint from image data

	Parameters:
		image_data (Image): image data
	"""
	return str(dhash(image_data))


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


def read_date(filepath: str) -> datetime:
	"""Read Modification Date from filepath"""
	epoch_time = os.path.getmtime(filepath)
	return datetime.fromtimestamp(epoch_time)


def read_location(filepath: str) -> Optional[str]:
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


def fingerprint_media(filepath: str):
	"""TODO"""
	if is_image(filepath):
		image = Image.open(filepath)
		return _compute_image_fingerprint(image)
	else:
		return _compute_video_hash()
