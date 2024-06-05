import pickle
from fastapi import FastAPI  # type: ignore
from model.types import PredictionModel

app = FastAPI()

try:
    model: PredictionModel = pickle.load("model.pkl")
except Exception as e:
    print("Error loading the model.")
    print(e)


@app.get("/status")
async def read_root():
    return {"message": "running"}


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    return model.predict(user_id)
