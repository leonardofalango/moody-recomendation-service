import pickle
from fastapi import FastAPI

app = FastAPI()

try:
    model = pickle.load('model.pkl')
except:
    print('Error loading the model.')

@app.get("/status")
async def read_root():
    return {"message": "running"}

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    return model.predict(user_id)

# @app.post("/items/")
# async def create_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
