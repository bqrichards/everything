import logging
import threading
from typing import List, Optional, Union
from dataclasses import dataclass
from geoalchemy2.shape import to_shape
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import FileStorage
from db import Media, session_scope
from db_actions import get_all_media, get_media_by_id, mark_media_modified, unflushed_changes
from paths import generate_random_media_filepath
from scan import get_extension, is_media_file, scan
from thumbnail import generate_thumbnails
import dateutil.parser
import pytz


def _encode_media(media: Union[Media, List[Media]]):
	"""Takes a Media or list of Media and converts the data to a JSON serializable format"""
	def get_new_media_date(m: Media):
		location = None
		if not m.location is None:
			p = to_shape(m.location)
			location = dict(lat=p.x, lon=p.y)

		return {
			'id': m.id,
			'date': None if m.date is None else m.date.replace(tzinfo=pytz.UTC).isoformat(),
			'location': location
		}

	if isinstance(media, list):
		return [get_new_media_date(m) for m in media]
	else:
		return get_new_media_date(media)


@dataclass
class Library:
	"""Response type for fetching Library"""

	"""All Media items"""
	media: List[Media]

	"""Whether there is modified Media to flush"""
	canFlush: bool


def get_library() -> Library:
	"""Fetches the Library"""
	all_media = get_all_media()
	encoded_media = _encode_media(all_media)
	can_flush = unflushed_changes()
	return Library(media=encoded_media, canFlush=can_flush)


def get_single_media(media_id: int) -> Optional[Media]:
	"""Fetches single Media by ID
	
	Parameters:
		media_id (int): Media ID
	
	Returns: Media if could be found, None if not
	"""
	media = get_media_by_id(media_id)
	if media is None:
		return None

	return _encode_media(media)


def _update_media_with_json(media: Media, new_media: dict):
	"""Updates piece of Media with new Media data in dictionary
	
	Parameters:
		media (Media): Media to alter
		new_media (dict): New Media data to apply
	"""
	if new_media['date'] is None:
		return

	utc_date = dateutil.parser.parse(new_media['date'])

	with session_scope() as session:
		fresh_media = session.query(Media).get(media.id)
		fresh_media.date = utc_date


def _update_media(media_id: int, new_media: dict) -> Optional[Media]:
	"""Updates piece of Media with new Media data in dictionary.
	Then marks this Media as modified since last flush.
	
	Parameters:
		media (Media): Media to alter
		new_media (dict): New Media data to apply
	
	Returns: Media if properly updated, None if no changes occurred
	"""
	media = get_media_by_id(media_id)
	if media is None:
		return None

	_update_media_with_json(media, new_media)

	mark_media_modified(media_id)

	return get_media_by_id(media_id)


def update_single_media(media_id: int, new_media: dict) -> Optional[Media]:
	"""Updates piece of Media with new Media data in dictionary
	
	Parameters:
		media (Media): Media to alter
		new_media (dict): New Media data to apply

	Returns: Media if able to be found and modified, None if not
	"""
	updated_media = _update_media(media_id, new_media)
	if updated_media is None:
		return None

	return _encode_media(updated_media)


def _scan_and_commit():
	"""Get all media items from the scanner and commit them to DB.
	Then generate thumbnails.
	"""
	scanned_media_items = scan()

	for media in scanned_media_items:
		try:
			with session_scope() as session:
				session.add(media)
		except IntegrityError:
			pass

	all_media_items = []
	with session_scope() as session:
		items = session.query(Media).all()
		session.expunge_all()
		all_media_items = items
	
	generate_thumbnails(all_media_items)


def scan_media_library():
	"""Starts thread to scan media library and generate thumbnails"""
	scan_thread = threading.Thread(target=_scan_and_commit)
	scan_thread.start()


def upload_new_media(files: 'list[FileStorage]'):
	"""Saves a list of files to media storage and rescans the library"""
	if not files:
		return False
	
	for file in files:
		# Check if file has valid extension
		if not is_media_file(file.filename):
			logging.info(f'Skipped {file.filename}, invalid media')
			continue

		filename = generate_random_media_filepath(get_extension(file.filename))
		logging.info(f'Uploading file {file.filename} -> {filename}')

		# Save
		file.save(filename)
	
	scan_media_library()

	return True
