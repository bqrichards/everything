from typing import List, Union
from thumbnail import generate_thumbnails, get_thumbnail_path, make_thumbnails_directory
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from dataclasses import dataclass
from db import ModificationRecord, metadata, Media
from flask_sqlalchemy import SQLAlchemy
import threading
from sqlalchemy.sql.functions import func
from scan import mime_from_ext, scan
from sqlalchemy.exc import IntegrityError
from flush_media import flush_media
import dateutil.parser
import logging
import pytz


logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/everything.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(metadata=metadata)
db.init_app(app)
with app.app_context():
	db.create_all()


def get_all_media():
	return db.session.query(Media).all()


def mark_media_modified(media_id):
	""" Note: Must be called within Flask app context """
	record = ModificationRecord(media_id=media_id)
	try:
		db.session.add(record)
		db.session.commit()
		logging.debug(f'Marked media_id seen: {media_id}')
	except IntegrityError:
		db.session.rollback()


def unflushed_changes():
	"""Returns whether there is media that has been modified since the last flush
	
		Note: Must be called within Flask app context
	"""
	modification_count = db.session.query(ModificationRecord).count()
	return modification_count > 0


def get_media_by_id(media_id):
	return db.session.query(Media).get(media_id)


def encode_media(media: Union[Media, List[Media]]):
	def get_new_media_date(m: Media):
		return {
			'id': m.id,
			'date': None if m.date is None else m.date.replace(tzinfo=pytz.UTC).isoformat()
		}

	if type(media) == list:
		return [get_new_media_date(m) for m in media]
	else:
		return get_new_media_date(media)


def jsonify_media(media: Union[Media, List[Media]]):
	if media is None:
		raise ValueError('media cannot be None')


def update_media_with_json(media: Media, new_media: dict):
	utc_date = None
	if new_media['date'] is not None:
		utc_date = dateutil.parser.parse(new_media['date'])

	media.date = utc_date


def update_media(media_id, new_media):
	media = get_media_by_id(media_id)
	if media is None:
		return None

	update_media_with_json(media, new_media)

	with app.app_context():
		db.session.commit()
		mark_media_modified(media_id)

	return get_media_by_id(media_id)


@dataclass
class HttpError:
	""" https://blog.restcase.com/rest-api-error-handling-problem-details-response """

	""" A human-readable description of the specific error. """
	detail: str

	""" a URL to a document describing the error condition """
	type: str

	""" A short, human-readable title for the general error type """
	title: str

	""" HTTP status code """
	status: int


def make_http_error(title: str, detail: str, status: int):
	return jsonify(HttpError(detail, 'about:blank', title, status)), status


@app.route('/api/flush')
def flush():
	with app.app_context():
		flush_media(db)

	return '', 204

@app.route('/api/thumbnail/<media_id>')
def get_thumbnail(media_id):
	media = get_media_by_id(media_id)
	if media is None:
		logging.warn(f'Grabbing thumbnail for nonexistant media {media_id}')
		return make_http_error('Missing Title', 'Media does not exist', 400)

	thumbnail_path = get_thumbnail_path(media)
	return send_file(thumbnail_path, mimetype=mime_from_ext(thumbnail_path))


@app.route('/api/media/visual/<media_id>')
def get_media_visual(media_id):
	media = get_media_by_id(media_id)
	if media is None:
		return make_http_error('Missing Title', 'Media does not exist', 400)

	return send_file(media.filepath, mimetype=mime_from_ext(media.filepath))


@app.route('/api/media/<media_id>')
def get_media(media_id):
	media = get_media_by_id(media_id)
	if media is None:
		return make_http_error('Missing Title', 'Media does not exist', 400)

	return jsonify(encode_media(media))


@app.route('/api/media/<media_id>/edit', methods=['PATCH'])
def edit_media(media_id):
	new_media = update_media(media_id, request.json)
	if new_media == None:
		return make_http_error('Invalid media', 'Invalid media', 400)

	return jsonify(encode_media(new_media)), 200
	

@app.route('/api/library')
def library():
	all_media = get_all_media()
	can_flush = unflushed_changes()
	return jsonify({
		'media': encode_media(all_media),
		'canFlush': can_flush
	})


def scan_and_commit():
	"""Get all media items from the scanner and commit them to DB.
	
	Then generate thumbnails.
	"""
	scanned_media_items = scan()

	with app.app_context():
		for media in scanned_media_items:
			try:
				db.session.add(media)
				db.session.commit()
			except IntegrityError:
				db.session.rollback()

	all_media_items = []
	with app.app_context():
		all_media_items = db.session.query(Media).all()

	generate_thumbnails(all_media_items)


if __name__ == '__main__':
	make_thumbnails_directory()

	scan_thread = threading.Thread(target=scan_and_commit)
	scan_thread.start()
	
	app.run(port=5000)
