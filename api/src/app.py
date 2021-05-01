from typing import List, Union
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from dataclasses import dataclass
from db import ModificationRecord, metadata, Media
from flask_sqlalchemy import SQLAlchemy
import threading
from sqlalchemy.exc import IntegrityError
from flush_media import flush_media
from scan import mime_from_ext, scan
import dateutil.parser
import logging
import pytz

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/everything.db'

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

def get_media_by_id(media_id):
	return db.session.query(Media).get(media_id)


def decode_media(media: Media):
	new_media = {
		'id': media.id,
		'date': None if media.date is None else media.date.replace(tzinfo=pytz.UTC).isoformat()
	}
	
	return new_media


def jsonify_media(media: Union[Media, List[Media]]):
	if media is None:
		raise ValueError('media cannot be None')

	if type(media) == list:
		return jsonify([decode_media(m) for m in media])
	else:
		return jsonify(decode_media(media))


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
		flush_media(db, complete=True)

	return jsonify(True)

@app.route('/api/thumbnail/<media_id>')
def get_thumbnail(media_id):
	media = get_media_by_id(media_id)
	if media is None:
		return make_http_error('Missing Title', 'Media does not exist', 400)

	return send_file(media.filepath, mimetype=mime_from_ext(media.filepath))


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

	return jsonify_media(media)


@app.route('/api/media/<media_id>/edit', methods=['PATCH'])
def edit_media(media_id):
	new_media = update_media(media_id, request.json)
	if new_media == None:
		return make_http_error('Invalid media', 'Invalid media', 400)

	return jsonify_media(new_media), 200


@app.route('/api/all')
def all():
	all_media = get_all_media()
	return jsonify_media(all_media)


def scan_and_commit():
	"""Get all media items from the scanner and commit them to DB"""
	media_items = scan()

	with app.app_context():
		for media in media_items:
			try:
				db.session.add(media)
				db.session.commit()
			except IntegrityError:
				db.session.rollback()


scan_thread = threading.Thread(target=scan_and_commit)
scan_thread.start()
