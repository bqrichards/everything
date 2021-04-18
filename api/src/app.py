from flask import Flask, jsonify
from flask_cors import CORS
from db import metadata, Media
from flask_sqlalchemy import SQLAlchemy
import threading
from sqlalchemy.exc import IntegrityError
from scan import scan

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/everything.db'

db = SQLAlchemy(metadata=metadata)
db.init_app(app)
with app.app_context():
	db.create_all()

def get_all_media():
	return db.session.query(Media).all()

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
