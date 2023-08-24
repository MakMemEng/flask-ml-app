import logging

import settings

logging.basicConfig(filename=settings.LOG_FILE, level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("running server")

    from app.models.user import User, database

    session = database.connect_db()
    u = User()
    u.name = "test"
    session.add(u)
    session.commit()
    session.close()
