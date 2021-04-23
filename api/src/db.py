from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import MetaData, Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

metadata = MetaData()
Base = declarative_base(metadata=metadata)

@dataclass
class Media(Base):
	__tablename__ = 'media'

	id: int
	filepath: str
	title: str
	comment: str
	date: datetime

	id = Column(Integer, primary_key=True)
	filepath = Column(Text, unique=True, nullable=False)
	title = Column(Text, nullable=False)
	comment = Column(Text, nullable=False)
	date = Column(DateTime)
	modification_record = relationship('ModificationRecord')


@dataclass
class ModificationRecord(Base):
	__tablename__ = 'modification_record'

	id: int
	media_id: int

	id = Column(Integer, primary_key=True)
	media_id = Column(Integer, ForeignKey('media.id'), unique=True, nullable=False)
