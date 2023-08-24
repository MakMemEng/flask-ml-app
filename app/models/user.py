from sqlalchemy import (
    Column,
    String,
    UniqueConstraint,
)

from app.models.db import BaseDatabase


class User(BaseDatabase):
    __tablename__ = "user"
    name = Column(String)
    UniqueConstraint(name)
