from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from model.dev_random_database import DevDatabaseController
from custom_recommendation_model import CustomRecommendationModel

app = FastAPI()
db_controller = DevDatabaseController()
recommendation_model = CustomRecommendationModel(db_controller)


@app.get("/v1/status")
async def read_root():
    return {"message": "running"}


@app.get("/v1/get_all")
async def read_root():
    return {"data": db_controller.get_all()}


@app.get("/v1/recommend/{user_id}")
async def get_user(user_id: str):
    return recommendation_model.recommend(user_id=user_id)
