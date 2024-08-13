from src.controllers.sqldb import SqliteController
from typing import Generator
import logging

logger = logging.getLogger("app_logger")


db_controller = SqliteController()
logger.info("Connection opened.")


def get_db_controller() -> Generator[SqliteController, None, None]:
    try:
        logger.debug("Returning db_controller.")
        yield db_controller

    except Exception as e:
        logger.error(f"Error: {e}")
