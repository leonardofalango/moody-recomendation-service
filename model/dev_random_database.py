import os
import json
import random
import logging
import pathlib
from typing import Iterable
from dotenv import load_dotenv
from model.types.repository import Repository
from model.types.dataclasses import User, RatePlace, Metrics

logger = logging.getLogger("app_logger")
load_dotenv()


class DevDatabaseController(Repository):
    def __init__(self) -> None:
        logger.info("Database initiating")

        population = int(os.environ.get("POPULATION", 5))

        self.user_data = []
        path = pathlib.Path("./")

        with open(path / "model" / "data" / "genres.json") as f:
            self.genres = json.load(f)["genres"]
        with open(path / "model" / "data" / "metrics.json") as f:
            self.labels = json.load(f)["metrics"]

        self.max_places = int(len(self.labels) / 2)
        self.max_interactions = int(self.max_places / 4)

        for i in range(population):
            self.user_data.append(self.__generate_fake_data(i))

        logger.info("Loaded database with %s data", population)

    def __generate_fake_data(self, user_id):
        age = random.randint(18, 19)
        music_genre = random.choice(self.genres)
        return User(
            user_id=str(user_id),
            age=age,
            music_genre=music_genre,
            metrics=[
                Metrics(
                    label=random.choice(self.labels),
                    interactions=random.randint(0, self.max_interactions),
                )
                for _ in range(random.randint(0, self.max_places))
            ],
        )

    def get_all(self) -> Iterable[User]:
        logger.info("Getting all users")
        return self.user_data

    def get_by_id(self, user_id: str) -> User:
        logger.info("Getting user from database")
        for user in self.user_data:
            if user.user_id == user_id:
                return user

    def update(self, user_id: str, data: User) -> None:
        logger.info("Updating user data")
        for user in self.user_data:
            if user.user_id == user_id:
                return user

    def create(self, data: User) -> None:
        logger.info("Creating user data")
        self.user_data.append(data)

    def delete(self, user_id: str) -> None:
        logger.info("Deleting user data")
        del self.user_data[user_id]

    def rate_place(self, rate_place: RatePlace) -> None:
        logger.info("Interaction with a place")
        user_data = self.get_by_id(rate_place.user_id)
        for metric in user_data.metrics:
            if metric.label == rate_place.label:
                metric.interactions += rate_place.interactions
                return

        user_data.metrics.append(
            Metrics(label=rate_place.label, interactions=rate_place.interactions)
        )
