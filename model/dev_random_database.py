import os
import json
import random
import logging
import pathlib
from typing import Iterable
from dotenv import load_dotenv
from model.types.repository import Repository
from model.types.basic_types import User, RatePlace, Metrics, Place

logger = logging.getLogger("app_logger")
load_dotenv()


class DevDatabaseController(Repository):
    def __init__(self) -> None:
        logger.info("Database initiating")

        population = int(os.environ.get("POPULATION", 15_000))

        self.user_data = []
        path = pathlib.Path("./")

        with open(path / "model" / "data" / "genres.json") as f:
            self.genres = json.load(f)["genres"]
        with open(path / "model" / "data" / "places.json", encoding="utf-8") as f:
            self.places = json.load(f)["places"]

        self.max_places = int(len(self.places) / 2)
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
                    place_id=random.choice(self.places)["place_id"],
                    user_id=str(user_id),
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
        self.user_data[user_id] = data

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
            if metric.place_id == rate_place.place_id:
                metric.interactions += rate_place.interactions
                return

        user_data.metrics.append(
            Metrics(
                user_id=rate_place.user_id,
                place_id=rate_place.place_id,
                interactions=rate_place.interactions,
            )
        )

    def get_all_places(self) -> Iterable[Place]:
        return self.places

    def get_place_by_id(self, place_id):
        for place in self.places:
            if place["place_id"] == place_id:
                return place
        return None

    def like_place(self, place_id):
        place = self.get_place_by_id(place_id)
        place["likes"] += 1
        return place
