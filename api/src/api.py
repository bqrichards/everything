from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import threading
import os
from exif import Image
from collections import namedtuple
from metadata import Metadata
from sqlalchemy.exc import IntegrityError
from dataclasses import dataclass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/everything.db'
db = SQLAlchemy(app)

image_extensions = ['.jpg', '.png', '.jpeg']
video_extensions = ['.mp4', '.mov']
allowed_extensions = image_extensions + video_extensions

@dataclass
class Media(db.Model):
	id: int
	filepath: str
	title: str
	comment: str
	date: str

	id = db.Column(db.Integer, primary_key=True)
	filepath = db.Column(db.Text, unique=True, nullable=False)
	title = db.Column(db.Text, nullable=False)
	comment = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime)

db.create_all()

media_directory = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'data')


def is_image(filepath: str) -> bool:
	_, ext = os.path.splitext(filepath)
	return ext.lower() in image_extensions


ValidMediaResult = namedtuple('ValidMediaResult', ['valid_media', 'is_image'])
def is_valid_media(filepath) -> ValidMediaResult(bool, Metadata):
	_, ext = os.path.splitext(filepath)
	valid = ext.lower() in allowed_extensions
	if not valid:
		return ValidMediaResult(False, None)
	
	if is_image(filepath):
		return ValidMediaResult(True, read_exif(filepath))
	else:
		return ValidMediaResult(True, None)


def read_exif(filepath: str) -> Metadata:
	with open(filepath, 'rb') as image_file:
		my_image = Image(image_file)
		return Metadata(my_image.get_all())


def scan():
	for root, _, files in os.walk(media_directory):
		for filename in files:
			filepath = os.path.join(root, filename)
			valid = is_valid_media(filepath)
			mediaItem = None
			if valid[0]:
				mediaItem = Media(filepath=filepath, title='', comment='')
			else:
				continue
			
			if valid[1] is not None:
				mediaItem.title = valid[1].title
				mediaItem.comment = valid[1].comment
				mediaItem.date = valid[1].date
			
			try:
				db.session.add(mediaItem)
				db.session.commit()
			except IntegrityError:
				db.session.rollback()

scan_thread = threading.Thread(target=scan)
scan_thread.start()

@app.route('/api/all')
def all():
	all_media = Media.query.all()
	return jsonify(all_media)

app.run(port=5000, debug=True)
