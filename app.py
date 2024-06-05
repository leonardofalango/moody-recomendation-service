import uvicorn
from fastapi import FastAPI
from model.dev_database_controller import DevDatabaseController
from custom_recommendation_model import CustomRecommendationModel

app = FastAPI()
db_controller = DevDatabaseController()
recommendation_model = CustomRecommendationModel(db_controller)


@app.get("/v1/status")
async def read_root():
    return {"message": "running"}


@app.get("/v1/recommend/{user_id}")
async def get_user(user_id: str):
    return recommendation_model.recommend(user_id=user_id)
