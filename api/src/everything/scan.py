import logging
import os
import typing
from everything.db import Media
from everything.media_io import is_media_file
from everything.paths import get_media_directory


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
				
			media_item = Media(filepath=filepath)

			retval.append(media_item)
	
	logging.info(f'Scanned {len(retval)} media items')
	return retval
