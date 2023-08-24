from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey

from app.models.db import BaseDatabase


class Rate(BaseDatabase):
    __tablename__ = "rate"
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    restaurant_id = Column(ForeignKey("restaurant.id", ondelete="CASCADE"))
    value = Column(Integer)
    UniqueConstraint(user_id, restaurant_id)
