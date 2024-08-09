from src.controllers.sqldb import SqliteController
from typing import Generator
import logging

logger = logging.getLogger("app_logger")


db_controller = SqliteController()


def get_db_controller() -> Generator[SqliteController, None, None]:
    logger.info("Connection opened.")
    try:
        logger.info("Returning db_controller.")
        yield db_controller

    except Exception as e:
        logger.error(f"Error: {e}")
