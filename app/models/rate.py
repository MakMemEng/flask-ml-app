import logging

from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey
import pandas as pd

import settings
from app.models.db import BaseDatabase, database
from app.models.restaurant import Restaurant

logger = logging.getLogger(__name__)

try:
    from surprise import SVD, Dataset, NormalPredictor, Reader
    from surprise.model_selection import cross_validate
except ImportError as ex:
    logger.error(str(ex))
    RECOMMEND_ENGINE_ENABLE = False

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
    def recommend_restaurant(user) -> list:
        if not settings.RECOMMEND_ENGINE_ENABLE:
            session = database.connect_db()
            recommend = [
                r.name
                for r in session.query(Restaurant).all()[:TOP_RECOMMEND_RESTAURANT_NUM]
            ]
            session.close()
            return recommend

        session = database.connect_db()
        df = pd.read_sql("SELECT user_id, restaurant_id, value from rate", session.bind)
        session.close()

        dataset_columns = ["user_id", "restaurant_id", "value"]
        reader = Reader()
        data = Dataset.load_from_df(df[dataset_columns], reader)
        try:
            cross_validate(NormalPredictor(), data, cv=2)
        except ValueError as ex:
            logger.error(str(ex))
            return None

        svd = SVD()
        trainset = data.build_full_trainset()
        svd.fit(trainset)

        predict_df = df.copy()
        item_id = "restaurant_id"
        predict_df["Predicted_Score"] = predict_df[item_id].apply(
            lambda x: svd.predict(user.id, x).est
        )
        predict_df = predict_df.sort_values(by=["Predicted_Score"], ascending=False)
        predict_df = predict_df.drop_duplicates(subset=item_id)

        if predict_df is None:
            return []

        recommended_restaurants = []
        for index, row in predict_df.iterrows():
            restaurant_id = int(row["restaurant_id"])
            restaurant = Restaurant.get(restaurant_id)
            recommended_restaurants.append(restaurant.name)

        return recommended_restaurants[:TOP_RECOMMEND_RESTAURANT_NUM]
