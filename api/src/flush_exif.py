import logging

from flask_sqlalchemy import SQLAlchemy
from db import Media, ModificationRecord
from exif import Image

from metadata import Metadata

def _write_exif_for_media(media: Media) -> bool:
	"""Writes data stored in the media model to its file
	
	Returns: `True` if metadata was able to be written to file, `False` if error occured
	"""
	metadata = Metadata.from_model(media)
	media_image = None
	# Read existing image
	with open(media.filepath, 'rb') as media_file:
		media_image = Image(media_file)
	
	metadata.write_to_image(media_image)

	# Write new metadata
	with open(media.filepath, 'wb') as media_file:
		media_file.write(media_image.get_file())

	return True

def flush_exif(db: SQLAlchemy, complete=False):
	"""Perform a flush of the database to disk

	Note: Must be called within app context.

	Args:
		db (SQLAlchemy): database of this app
		complete (bool, optional): TODO whether to flush all media items to disk.
		Default is `False`, meaning only flush media in modification record.
	"""
	logging.info(f'Flushing database with complete={complete}')
	modifications = db.session.query(ModificationRecord.media_id).all()
	modified_media_ids = [result[0] for result in modifications]
	if len(modified_media_ids) == 0:
		logging.info('No media to flush')
		return

	modified_media_ids.sort()
	modified_media = db.session.query(Media).filter(Media.id.in_(modified_media_ids)).all()

	successful_writes = []
	unsuccessful_writes = []
	for media in modified_media:
		if (_write_exif_for_media(media)):
			successful_writes.append(media.id)
		else:
			unsuccessful_writes.append(media.id)

	# Remove successful writes from modification table
	db.session.query(ModificationRecord).filter(ModificationRecord.media_id.in_(successful_writes)).delete(synchronize_session=False)
	db.session.commit()
	db.session.expire_all()

	if len(successful_writes) == len(modified_media_ids):
		logging.info('All modifications successfully flushed')
	else:
		logging.warn(f'Could not write following media_ids: {", ".join([str(i) for i in unsuccessful_writes])}')
