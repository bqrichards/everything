import logging
from typing import List
from db import Media, ModificationRecord, session_scope
from sqlalchemy.exc import IntegrityError


def mark_media_modified(media_id: int):
	""" Note: Must be called within Flask app context """
	try:
		record = ModificationRecord(media_id=media_id)
		with session_scope() as session:
			session.add(record)
	except IntegrityError:
		logging.info(f'Media ID {media_id} already marked modified')


def get_media_by_id(media_id: int) -> Media:
	"""TODO docstring"""
	with session_scope() as session:
		retval = session.query(Media).get(media_id)
		session.expunge_all()
		return retval


def get_all_media() -> List[Media]:
	"""TODO docstring"""
	with session_scope() as session:
		retval = session.query(Media).all()
		session.expunge_all()
		return retval


def unflushed_changes() -> bool:
	"""Returns whether there is media that has been modified since the last flush
	
		Note: Must be called within Flask app context
	"""
	with session_scope() as session:
		modification_count = session.query(ModificationRecord).count()
		return modification_count > 0
