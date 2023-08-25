from sqlalchemy import Column, String, UniqueConstraint

from app.models.db import BaseDatabase, database


class Restaurant(BaseDatabase):
    __tablename__ = "restaurant"
    name = Column(String)
    UniqueConstraint(name)

    @staticmethod
    def get(restaurant_id):
        session = database.connect_db()
        row = session.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if row:
            session.close()
            return row
        return None

    @staticmethod
    def get_or_create(name):
        session = database.connect_db()
        row = session.query(Restaurant).filter(Restaurant.name == name).first()
        if row:
            session.close()
            return row

        restaurant = Restaurant(name=name)
        session.add(restaurant)
        session.commit()
        # return restaurant  とすると,restaurant.idを取得しないまま,呼び出してしまう
        # dbにcommitしたデータを再度呼び出す必要がある
        row = session.query(Restaurant).filter(Restaurant.name == name).first()
        session.close()
        return row
