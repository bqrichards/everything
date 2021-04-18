import os
from collections import namedtuple
from typing import List
from exif import Image
from metadata import Metadata
from db import Media

image_extensions = ['.jpg', '.png', '.jpeg']
video_extensions = ['.mp4', '.mov']
allowed_extensions = image_extensions + video_extensions

media_directory = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'data')

def _is_image(filepath: str) -> bool:
	_, ext = os.path.splitext(filepath)
	return ext.lower() in image_extensions


def _read_exif(filepath: str) -> Metadata:
	with open(filepath, 'rb') as image_file:
		my_image = Image(image_file)
		return Metadata(my_image.get_all())


ValidMediaResult = namedtuple('ValidMediaResult', ['valid_media', 'image_metadata'])
def _is_valid_media(filepath) -> ValidMediaResult(bool, Metadata):
	_, ext = os.path.splitext(filepath)
	valid = ext.lower() in allowed_extensions
	if not valid:
		return ValidMediaResult(False, None)
	
	if _is_image(filepath):
		return ValidMediaResult(True, _read_exif(filepath))
	else:
		return ValidMediaResult(True, None)


def scan() -> List[Media]:
	retval = []

	for root, _, files in os.walk(media_directory):
		for filename in files:
			filepath = os.path.join(root, filename)
			valid = _is_valid_media(filepath)
			mediaItem = None
			if valid[0]:
				mediaItem = Media(filepath=filepath, title='', comment='')
			else:
				continue
			
			if valid[1] is not None:
				mediaItem.title = valid[1].title
				mediaItem.comment = valid[1].comment
				mediaItem.date = valid[1].date
			
			retval.append(mediaItem)
	
	return retval
