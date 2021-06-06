from sqlalchemy import MetaData, Column, Integer, Text, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.event.api import listen
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import select, func
from contextlib import contextmanager
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKBElement
from dataclasses import dataclass
from datetime import datetime
import logging


metadata = MetaData()
Base = declarative_base(metadata=metadata)


_engine = None
_Session = None


@dataclass
class ModificationRecord(Base):
	__tablename__ = 'modification_record'

	id: int
	media_id: int

	id = Column(Integer, primary_key=True)
	media_id = Column(Integer, ForeignKey('media.id'), unique=True, nullable=False)


@dataclass
class Media(Base):
	__tablename__ = 'media'

	id: int
	filepath: str
	date: datetime
	location: WKBElement
	fingerprint: str

	id = Column(Integer, primary_key=True)
	filepath = Column(Text, unique=True, nullable=False, index=True)
	date = Column(DateTime)
	location = Column(Geometry(geometry_type='POINT', management=True))
	fingerprint = Column(Text)
	modification_record = relationship(ModificationRecord)


def initialize_db(db_connection_string):
	"""Creates database engine and sessionmaker"""
	global _engine
	global _Session
	_engine = create_engine(db_connection_string)

	def load_spatialite(dbapi_conn, connection_record):
		dbapi_conn.enable_load_extension(True)
		dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')
	
	listen(_engine, 'connect', load_spatialite)

	# https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
	# Initialize SpatiaLite
	conn = _engine.connect()
	try:
		conn.execute(select([func.InitSpatialMetaData()]))
	except OperationalError as e:
		logging.error('Error calling InitSpatialMetaData', exc_info=e)
	conn.close()

	_Session = sessionmaker(bind=_engine)
	Base.metadata.create_all(_engine)


# https://docs.sqlalchemy.org/en/13/orm/session_basics.html
@contextmanager
def session_scope():
	session = _Session()
	try:
		yield session
		session.commit()
	except:
		session.rollback()
		raise
	finally:
		session.close()
