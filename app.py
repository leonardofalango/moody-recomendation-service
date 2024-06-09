import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Path, Query
from model.types.dataclasses import User, RatePlace
from model.dev_random_database import DevDatabaseController
from custom_recommendation_model import CustomRecommendationModel

load_dotenv()
logging.getLogger("app_logger")
logging.basicConfig(
    filename=os.environ.get("LOGGER_PATH", ""),
    datefmt="%Y-%m-%d | %H:%M:%S |",
    level=logging.DEBUG,
)

app = FastAPI()
db_controller = DevDatabaseController()
recommendation_model = CustomRecommendationModel(db_controller)


@app.get("/v1/status")
async def status():
    """
    Get the status of the API.
    """
    return {"message": "running"}


@app.post("/v1/user")
async def create_user(user: User):
    """
    Create a new user.
    """
    db_controller.create(user)


@app.get("/v1/user/{user_id}")
async def get_by_id(user_id: str = Path(..., description="The ID of the user")):
    """
    Get user data by ID.
    """
    return {"data": db_controller.get_by_id(user_id=user_id)}


@app.patch("/v1/user/{user_id}")
async def update_user(user_id: str, user: User):
    """
    Update a user.
    """
    db_controller.update(user_id=user_id, data=user)


@app.delete("/v1/user/{user_id}")
async def delete_user(user_id: str = Path(..., description="The ID of the user")):
    """
    Delete a user.
    """
    db_controller.delete(user_id=user_id)


@app.get("/v1/recommend/{user_id}")
async def get_recommendation(
    user_id: str = Path(..., description="The ID of the user")
):
    """
    Get recommendations for a user.
    """
    return {
        "recommendation": recommendation_model.recommend(user_id=user_id),
    }


@app.delete("/v1/clear_cache/")
async def clear_cache(user_id: str = None):
    """
    Clear the cache.
    """
    recommendation_model.clear_cache(user_id=user_id)
    return {"message": "success"}


@app.post("/v1/rate/")
async def rate_place(rate_place: RatePlace):
    """
    Rate a place.
    """
    db_controller.rate_place(rate_place)
    await clear_cache(user_id=rate_place.user_id)
    return {"message": "success"}


@app.get("/v1/recommend/{user_id}/params")
async def get_recommendation_params(
    user_id: str = Path(..., description="The ID of the user"),
    n_recommendations: int = Query(..., description="Number of recommendations to get"),
    k_neighboors: int = Query(..., description="Number of neighbors to consider"),
):
    """
    Get recommendations for a user with specified parameters.
    """
    return recommendation_model.recommend(
        user_id=user_id, n_recommendations=n_recommendations, k_neighboors=k_neighboors
    )


@app.get("/")
async def read_root():
    """
    Root endpoint.
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
