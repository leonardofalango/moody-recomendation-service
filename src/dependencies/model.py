from fastapi import Depends
from typing import Generator
from src.dependencies.db import get_db_controller
from src.models.custom_recommendation_model import CustomRecommendationModel


def get_recommendation_model(
    db_controller=Depends(get_db_controller),
) -> Generator[CustomRecommendationModel, None, None]:
    recommendation_model = CustomRecommendationModel(db_controller=db_controller)
    try:
        yield recommendation_model
    finally:
        del recommendation_model
