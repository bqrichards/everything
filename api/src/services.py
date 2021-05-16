import threading
from typing import List, TypedDict, Union
from geoalchemy2.shape import to_shape
import pytz
from sqlalchemy.exc import IntegrityError
from db import Media, session_scope
from db_actions import get_all_media, get_media_by_id, mark_media_modified, unflushed_changes
import dateutil.parser
from scan import scan
from thumbnail import generate_thumbnails


def encode_media(media: Union[Media, List[Media]]):
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

	if type(media) == list:
		return [get_new_media_date(m) for m in media]
	else:
		return get_new_media_date(media)


class Library(TypedDict):
	media: List[Media]
	canFlush: bool


def get_library() -> Library:
	all_media = get_all_media()
	encoded_media = encode_media(all_media)
	can_flush = unflushed_changes()
	return Library(media=encoded_media, canFlush=can_flush)


def get_single_media(media_id: int) -> Union[Media, None]:
	media = get_media_by_id(media_id)
	if media is None:
		return None

	return encode_media(media)


def _update_media_with_json(media: Media, new_media: dict):
	if new_media['date'] is None:
		return

	utc_date = dateutil.parser.parse(new_media['date'])

	with session_scope() as session:
		fresh_media = session.query(Media).get(media.id)
		fresh_media.date = utc_date


def _update_media(media_id: int, new_media):
	media = get_media_by_id(media_id)
	if media is None:
		return None

	_update_media_with_json(media, new_media)

	mark_media_modified(media_id)

	return get_media_by_id(media_id)


def update_single_media(media_id: int, new_media) -> Union[Media, None]:
	updated_media = _update_media(media_id, new_media)
	if updated_media is None:
		return None

	return encode_media(updated_media)


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
	"""TODO docstring"""
	scan_thread = threading.Thread(target=_scan_and_commit)
	scan_thread.start()

