import datetime

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings


class Database(object):
    def __init__(self) -> None:
        self.engine = create_engine(f"sqlite:///{settings.DB_NAME}")
        self.connect_db()

    def connect_db(self) -> sessionmaker:
        Base.metadata.create_all(self.engine)
        session = sessionmaker(self.engine)
        return session()


Base = declarative_base()
database = Database()


class BaseDatabase(Base):
    __abstract__ = True  # Tableを作成しない設定
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
