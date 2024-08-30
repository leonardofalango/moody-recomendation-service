import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from jobs import start_scheduler
from fastapi.middleware.cors import CORSMiddleware

from src.routes import (
    label_router,
    user_router,
    place_router,
    recommendation_router,
    default_router,
    api_key,
)

from uvicorn.config import Config
from uvicorn.main import Server


load_dotenv()
logging.getLogger("app_logger")
logging.basicConfig(datefmt="%Y-%m-%d | %H:%M:%S |", level=logging.DEBUG)

app = FastAPI()

config = Config(app, loop="asyncio", timeout_keep_alive=600)
server = Server(config=config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://exploremoody.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(api_key.api_key_middleware)

app.include_router(default_router.router, tags=["default"])
app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(place_router.router, prefix="/place", tags=["place"])
app.include_router(label_router.router, prefix="/label", tags=["label"])
app.include_router(
    recommendation_router.router, prefix="/recommendation", tags=["recommendation"]
)

start_scheduler(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
