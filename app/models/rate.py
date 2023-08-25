from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey

import settings
from app.models.db import BaseDatabase, database
from app.models.restaurant import Restaurant

TOP_RECOMMEND_RESTAURANT_NUM = 10


class Rate(BaseDatabase):
    __tablename__ = "rate"
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    restaurant_id = Column(ForeignKey("restaurant.id", ondelete="CASCADE"))
    value = Column(Integer)
    UniqueConstraint(user_id, restaurant_id)

    @staticmethod
    def update_or_create(user, restaurant, value):
        session = database.connect_db()
        rate = (
            session.query(Rate)
            .filter(Rate.user_id == user.id, Rate.restaurant_id == restaurant.id)
            .first()
        )
        if rate:
            rate.value = value
            session.add(rate)
            session.commit()
            session.close()
            return rate
        rate = Rate(user_id=user.id, restaurant_id=restaurant.id, value=value)
        session.add(rate)
        session.commit()
        session.close()

    @staticmethod
    def recommend_restaurant(user):
        if not settings.RECOMMEND_ENGINE_ENABLE:
            session = database.connect_db()
            session.query(Restaurant).all()
            recommend = [
                r.name
                for r in session.query(Restaurant).all()[:TOP_RECOMMEND_RESTAURANT_NUM]
            ]
            session.close()
            return recommend
