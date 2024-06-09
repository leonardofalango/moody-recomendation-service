import json
import random
import logging
import pathlib
from typing import Iterable
from model.types.dataclasses import UserData
from model.types.repository import Repository

logger = logging.getLogger("app_logger")


class DevDatabaseController(Repository):
    def __init__(self, population: int = 100) -> None:
        logger.info("Database initiating")

        self.user_data = {}
        path = pathlib.Path("./")

        with open(path / "model" / "data" / "genres.json") as f:
            self.genres = json.load(f)["genres"]
        with open(path / "model" / "data" / "metrics.json") as f:
            self.metrics = json.load(f)["metrics"]

        self.max_places = int(len(self.metrics) / 2)
        self.max_interactions = int(self.max_places / 4)

        for i in range(population):
            self.user_data[str(i)] = self.__generate_fake_data(i)

        logger.info("Loaded database with %s data", population)

    def __generate_fake_data(self, user_id):
        age = random.randint(18, 19)
        music_genre = random.choice(self.genres)
        return {
            "user_id": str(user_id),
            "age": age,
            "music_genre": music_genre,
            "metrics": [
                dict(
                    random.choice(self.metrics),
                    interactions=random.randint(0, self.max_interactions),
                )
                for x in range(random.randint(0, self.max_places))
            ],
        }

    def get_all(self) -> Iterable[UserData]:
        logger.info("Getting all users")
        return self.user_data

    def get_by_id(self, user_id: str) -> UserData:
        logger.info("Getting user from database")
        return self.user_data[user_id]

    def update(self, user_id: str, data: UserData) -> None:
        logger.info("Updating user data")
        self.user_data[user_id] = data

    def create(self, data: UserData) -> None:
        logger.info("Creating user data")
        self.user_data[data["user_id"]] = data

    def delete(self, user_id: str) -> None:
        logger.info("Deleting user data")
        del self.user_data[user_id]

    def rate_place(self, user_id: str, place_id: str, rate: int = 1) -> None:
        logger.info("Interaction with a place")
        user_data = self.user_data[user_id]
        for metric in user_data["metrics"]:
            if metric["label"] == place_id:
                metric["interactions"] += rate
                return

        user_data["metrics"].append({"label": place_id, "interactions": rate})
