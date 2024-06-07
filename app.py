import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Path, Query
from model.dev_random_database import DevDatabaseController
from custom_recommendation_model import CustomRecommendationModel

load_dotenv()
logging.getLogger("app_logger")
logging.basicConfig(
    filename=os.environ.get("LOGGER_PATH", ""),
    datefmt="%Y-%m-%d | %H:%M:%S |",
    level=logging.DEBUG,
)

population = int(os.environ.get("POPULATION_DEV", 15_000))
app = FastAPI()
db_controller = DevDatabaseController(population=population)
recommendation_model = CustomRecommendationModel(db_controller)


@app.get("/v1/status")
async def status():
    """
    Get the status of the API.
    """
    return {"message": "running"}


@app.get("/v1/user/{user_id}")
async def get_by_id(user_id: str = Path(..., description="The ID of the user")):
    """
    Get user data by ID.
    """
    return {"data": db_controller.get_by_id(user_id=user_id)}


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
