from src.controllers.moodydb import PostgressController
from typing import Generator
import logging

logger = logging.getLogger("app_logger")


db_controller = PostgressController()
logger.info("Connection opened.")


def get_db_controller() -> Generator[PostgressController, None, None]:
    try:
        logger.debug("Returning db_controller.")
        yield db_controller

    except Exception as e:
        logger.error(f"Error: {e}")
