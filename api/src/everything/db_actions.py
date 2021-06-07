import logging
from typing import List
from sqlalchemy.sql.functions import func
from everything.db import Media, ModificationRecord, session_scope
from sqlalchemy.exc import IntegrityError


def get_duplicates_exist():
	"""Returns whether any duplicate media exists in the database"""
	with session_scope() as session:
		media_count = session.query(func.count(Media.id))
		unique_fingerprint_count = session.query(func.count(func.distinct(Media.fingerprint)))
		return media_count != unique_fingerprint_count


def mark_media_modified(media_id: int):
	"""Creates a ModificationRecord for a Media item by ID
	
	Parameters:
		media_id (int): ID of Media
	"""
	try:
		record = ModificationRecord(media_id=media_id)
		with session_scope() as session:
			session.add(record)
	except IntegrityError:
		logging.info(f'Media ID {media_id} already marked modified')


def get_media_by_id(media_id: int) -> Media:
	"""Query the database for one Media item by ID
	
	Parameters:
		media_id (int): ID of Media
	
	Returns: Media with ID
	"""
	with session_scope() as session:
		retval = session.query(Media).get(media_id)
		session.expunge_all()
		return retval


def get_all_media() -> List[Media]:
	"""Query the database for all Media items
	
	Returns: All Media in database
	"""
	with session_scope() as session:
		retval = session.query(Media).all()
		session.expunge_all()
		return retval


def unflushed_changes() -> bool:
	"""Checks whether there is media that has been modified since the last flush
	
		Returns: whether unflushed media exists
	"""
	with session_scope() as session:
		modification_count = session.query(ModificationRecord).count()
		return modification_count > 0
