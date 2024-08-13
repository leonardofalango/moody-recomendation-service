from fastapi import Depends
from typing import Generator, Optional
from src.dependencies.db import get_db_controller
from src.models.custom_recommendation_model import CustomRecommendationModel


class RecommendationModelSingleton:
    _instance: Optional[CustomRecommendationModel] = None

    @classmethod
    def get_instance(cls, db_controller) -> CustomRecommendationModel:
        if cls._instance is None:
            cls._instance = CustomRecommendationModel(db_controller=db_controller)
        return cls._instance


def get_recommendation_model(
    db_controller=Depends(get_db_controller),
) -> Generator[CustomRecommendationModel, None, None]:
    recommendation_model = RecommendationModelSingleton.get_instance(
        db_controller=db_controller
    )
    try:
        yield recommendation_model
    finally:
        del recommendation_model
