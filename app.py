from fastapi import FastAPI
from model.dev_random_database import DevDatabaseController
from custom_recommendation_model import CustomRecommendationModel

population = 15_000
app = FastAPI()
db_controller = DevDatabaseController(population=population)
recommendation_model = CustomRecommendationModel(db_controller)


@app.get("/v1/status")
async def read_root():
    return {"message": "running"}


@app.get("/v1/get_all")
async def read_root():
    return {"data": db_controller.get_all()}


@app.get("v1/user/{user_id}")
async def get_by_id(user_id: str):
    return {"data": db_controller.get_by_id(user_id=user_id)}


@app.get("/v1/recommend/{user_id}")
async def get_user(user_id: str):
    return {
        "recommendation": recommendation_model.recommend(user_id=user_id),
    }


@app.get("/v1/recommend/{user_id}/{n_recommendations}/{k_neighboors}")
async def get_user(user_id: str, n_recommendations: int, k_neighboors: int):
    return recommendation_model.recommend(
        user_id=user_id, n_recommendations=n_recommendations, k_neighboors=k_neighboors
    )


@app.get("/v1/recommend/{user_id}/places={n_recommendations}")
async def get_user(user_id: str, n_recommendations: int):
    return recommendation_model.recommend(
        user_id=user_id, n_recommendations=n_recommendations, k_neighboors=3
    )


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
