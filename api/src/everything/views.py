import os
import logging
from everything import app
from everything.paths import _FRONTEND_URL_ENV_KEY
from everything.services import get_library, upload_new_media
from flask import request, send_file, jsonify, redirect
from everything.services import get_single_media, update_single_media
from everything.thumbnail import get_thumbnail_path
from everything.db_actions import get_media_by_id
from everything.flush_media import flush_media
from everything.media_io import mime_from_ext
from everything.models import HttpError


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


@app.route('/api/upload-media', methods=['POST'])
def upload_media():
	if upload_new_media(request.files.getlist('file[]')):
		return redirect(os.getenv(_FRONTEND_URL_ENV_KEY))
	else:
		return jsonify(False, 400)
