from everything.services import scan_media_library
from everything.paths import initialize_paths, get_database_path
from everything.db import initialize_db
from flask_cors import CORS
from everything import app
import logging


logging.getLogger().setLevel(logging.DEBUG)


initialize_paths()


database_uri = f'sqlite:///{get_database_path()}'
logging.info(f'Using database uri {database_uri}')


CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


initialize_db(database_uri)


import everything.views


scan_media_library()
