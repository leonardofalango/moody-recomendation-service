import os
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from src.routes import (
    label_router,
    user_router,
    place_router,
    recommendation_router,
    default_router,
)

from uvicorn.config import Config
from uvicorn.main import Server


load_dotenv()
logging.getLogger("app_logger")
logging.basicConfig(
    filename=os.environ.get("LOGGER_PATH", ""),
    datefmt="%Y-%m-%d | %H:%M:%S |",
    level=logging.DEBUG,
)

app = FastAPI()

config = Config(app, loop="asyncio", timeout_keep_alive=600)
server = Server(config=config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://moody-prot.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(default_router.router, tags=["default"])

app.include_router(user_router.router, prefix="/user", tags=["user"])
app.include_router(place_router.router, prefix="/place", tags=["place"])
app.include_router(label_router.router, prefix="/label", tags=["label"])
app.include_router(
    recommendation_router.router, prefix="/recommendation", tags=["recommendation"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
