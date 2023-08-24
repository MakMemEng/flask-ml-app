from sqlalchemy import Column, String, UniqueConstraint

from app.models.db import BaseDatabase


class Restaurant(BaseDatabase):
    __tablename__ = "restaurant"
    name = Column(String)
    UniqueConstraint(name)
