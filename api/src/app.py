import os
from db_actions import get_media_by_id
from models import HttpError
from services import get_library, get_single_media, scan_media_library, update_single_media
from thumbnail import get_thumbnail_path
from flask import Flask, jsonify, send_file, request
from paths import initialize_paths, get_database_path
from flask_cors import CORS
from db import initialize_db
from scan import mime_from_ext
from flush_media import flush_media
import logging


logging.getLogger().setLevel(logging.DEBUG)


initialize_paths()


database_uri = f'sqlite:///{get_database_path()}'
logging.info(f'Using database uri {database_uri}')


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


initialize_db(database_uri)


def make_http_error(title: str, detail: str, status: int):
	return jsonify(HttpError(detail, 'about:blank', title, status)), status


@app.route('/api/flush')
def flush():
	flush_media()
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
	media = get_single_media(media_id)
	if media is None:
		return make_http_error('Missing Title', 'Media does not exist', 400)

	return jsonify(media)


@app.route('/api/media/<media_id>/edit', methods=['PATCH'])
def edit_media(media_id):
	new_media = update_single_media(media_id, request.json)
	if new_media is None:
		return make_http_error('Invalid media', 'Invalid media', 400)

	return jsonify(new_media)
	

@app.route('/api/library')
def library():
	library = get_library()
	return jsonify(library)


scan_media_library()
