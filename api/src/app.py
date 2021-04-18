from flask import Flask, jsonify, send_file
from flask_cors import CORS
from dataclasses import dataclass
from db import metadata, Media
from flask_sqlalchemy import SQLAlchemy
import threading
from sqlalchemy.exc import IntegrityError
from scan import mime_from_ext, scan

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/everything.db'

db = SQLAlchemy(metadata=metadata)
db.init_app(app)
with app.app_context():
	db.create_all()

def get_all_media():
	return db.session.query(Media).all()

def get_media_by_id(media_id):
	return db.session.query(Media).get(media_id)

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

def make_http_error(detail: str, type: str, title: str, status: int):
	return jsonify(HttpError(detail, type, title, status)), status

@app.route('/api/thumbnail/<media_id>')
def get_thumbnail(media_id):
	media = get_media_by_id(media_id)
	if media is None:
		return make_http_error('Media does not exist', 'about:blank', 'Missing Title', 400)

	return send_file(media.filepath, mimetype=mime_from_ext(media.filepath))

@app.route('/api/media/visual/<media_id>')
def get_media_visual(media_id):
	media = get_media_by_id(media_id)
	if media is None:
		return make_http_error('Media does not exist', 'about:blank', 'Missing Title', 400)

	return send_file(media.filepath, mimetype=mime_from_ext(media.filepath))

@app.route('/api/media/<media_id>')
def get_media(media_id):
	media = get_media_by_id(media_id)
	if media is None:
		return make_http_error('Media does not exist', 'about:blank', 'Missing Title', 400)

	return jsonify(media)

@app.route('/api/all')
def all():
	all_media = get_all_media()
	return jsonify(all_media)

def scan_and_commit():
	""" Get all media items from the scanner and commit them to DB """
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
