import logging

from flask_sqlalchemy import SQLAlchemy
from db import Media, ModificationRecord

from media_io import write_date_to_media


def _write_media(media: Media) -> bool:
	"""Writes data stored in the media model to its file
	
	Returns: `True` if metadata was able to be written to file, `False` if error occured
	"""
	if media.date is not None:
		try:
			write_date_to_media(media)
			return True
		except Exception as e:
			print(f'Error while writing media date - {e}')
			return False
	

def flush_media(db: SQLAlchemy, complete=False):
	"""Perform a flush of the database to disk

	Note: Must be called within app context.

	Args:
		db (SQLAlchemy): database of this app
		complete (bool, optional): TODO whether to flush all media items to disk.
		Default is `False`, meaning only flush media in modification record.
	"""
	logging.info(f'Flushing database with complete={complete}')
	media_to_write = []
	if not complete:
		modifications = db.session.query(ModificationRecord.media_id).all()
		modified_media_ids = [result[0] for result in modifications]
		if len(modified_media_ids) == 0:
			logging.info('No media to flush')
			return

		modified_media_ids.sort()
		media_to_write = db.session.query(Media).filter(Media.id.in_(modified_media_ids)).all()
	else:
		media_to_write = db.session.query(Media).all()
	

	successful_writes = []
	unsuccessful_writes = []
	for media in media_to_write:
		if (_write_media(media)):
			successful_writes.append(media.id)
		else:
			unsuccessful_writes.append(media.id)

	# Remove successful writes from modification table
	if not complete:
		db.session.query(ModificationRecord).filter(ModificationRecord.media_id.in_(successful_writes)).delete(synchronize_session=False)
		db.session.commit()
		db.session.expire_all()

		if len(successful_writes) == len(modified_media_ids):
			logging.info('All modifications successfully flushed')
		else:
			logging.warn(f'Could not write following media_ids: {", ".join([str(i) for i in unsuccessful_writes])}')
	else:
		logging.info('Flushed database')