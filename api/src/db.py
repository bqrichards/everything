from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import MetaData, Column, Integer, Text, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import ForeignKey

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

	id = Column(Integer, primary_key=True)
	filepath = Column(Text, unique=True, nullable=False)
	date = Column(DateTime)
	modification_record = relationship(ModificationRecord)


def initialize_db(db_connection_string):
	global _engine
	global _Session
	_engine = create_engine(db_connection_string, echo=True)
	_Session = sessionmaker(bind=_engine)
	Base.metadata.create_all(_engine)


def get_engine():
	return _engine


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
