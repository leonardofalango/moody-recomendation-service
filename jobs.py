from apscheduler.schedulers.background import BackgroundScheduler
from src.dependencies.db import get_db_controller
from src.models.custom_recommendation_model import CustomRecommendationModel
from fastapi import FastAPI
from datetime import datetime
import logging

logger = logging.getLogger("app_logger")


def get_all_users_recommendation():
    logger.info(f"Job executed at: {datetime.now()}")

    db_controller = next(get_db_controller())
    try:
        recommendation_model = CustomRecommendationModel(db_controller=db_controller)
        recommendation_model.recommend_all_users()
    finally:
        del recommendation_model


def start_scheduler(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        get_all_users_recommendation,
        "interval",
        hours=8,
        next_run_time=datetime.now(),
    )
    scheduler.start()
