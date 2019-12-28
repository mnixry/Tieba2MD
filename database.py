from typing import List

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

Base = declarative_base()


class Contents(Base):
    __tablename__ = 'contents'
    row = Column(Integer, primary_key=True)
    page = Column(Integer, index=True)
    data = Column(String)


class Replies(Base):
    __tablename__ = 'replies'
    row = Column(Integer, primary_key=True)
    rid = Column(Integer, index=True, unique=True)
    page = Column(Integer, index=True)
    data = Column(String)


class Floors(Base):
    __tablename__ = 'floors'
    row = Column(Integer, primary_key=True)
    rid = Column(Integer, index=True, unique=True)
    floor = Column(Integer, index=True)
    pubtime = Column(Integer, index=True)
    author = Column(Integer, index=True)
    content = Column(String)


class ChildFloors(Base):
    __tablename__ = 'child_floors'
    row = Column(Integer, primary_key=True)
    rid = Column(Integer, index=True)
    pubtime = Column(Integer, index=True)
    author = Column(Integer, index=True)
    content = Column(String)


class _database:
    def __init__(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.sessionFactory = sessionmaker(bind=self.engine)
        self.originSession = scoped_session(self.sessionFactory)


StorageDatabase = _database
