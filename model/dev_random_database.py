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

        population = int(os.environ.get("POPULATION", 100))

        self.user_data: list[User] = []
        path = pathlib.Path("./")

        with open(path / "model" / "data" / "genres.json") as f:
            self.genres = json.load(f)["genres"]
        with open(path / "model" / "data" / "places.json", encoding="utf-8") as f:
            places: list[object] = json.load(f)["places"]
        with open(path / "model" / "data" / "labels.json", encoding="utf-8") as f:
            self.labels: list[object] = json.load(f)["labels"]

        self.places = self.__populate_places(places)
        self.n_places = 20
        self.max_interactions = 2

        for i in range(population):
            self.user_data.append(self.__generate_fake_data(i))

        logger.info("Loaded database with %s data", population)

    def __populate_places(self, places: list[object]) -> list[Place]:
        place_list = []
        for place in places:
            place_list.append(
                Place(
                    place_id=place["place_id"],
                    name=place["name"],
                    location=place["location"],
                    rating=place["rating"],
                    likes=place["likes"],
                    image=place["image"],
                )
            )
        return place_list

    def __generate_fake_data(self, user_id: str):
        age = random.randint(18, 19)
        metrics = self.__generate_metrics(user_id)
        return User(
            user_id=str(user_id),
            age=age,
            music_genre=self.__get_music_genre(metrics),
            perfil=self.__get_perfil(metrics),
            metrics=metrics,
        )

    def __generate_metrics(self, user_id: str) -> list[Metrics]:
        first_place = random.choice(self.places)
        k = first_place.name.split(" ")[0]
        ms = [
            Metrics(
                place_id=first_place.place_id,
                user_id=str(user_id),
                interactions=2,
            )
        ]

        similiar_places = [place for place in self.places if k in place.name]
        for _ in range(
            random.randint(int(len(similiar_places) / 3), len(similiar_places))
        ):
            place_id = random.choice(similiar_places).place_id

            if place_id == any(similiar_places):
                continue

            ms.append(
                Metrics(
                    place_id=place_id,
                    user_id=str(user_id),
                    interactions=1,
                )
            )
        for _ in range(self.n_places):
            place_id = random.choice(self.places).place_id

            if place_id == any(ms):
                continue

            ms.append(
                Metrics(
                    place_id=place_id,
                    user_id=str(user_id),
                    interactions=random.randint(0, 1),
                )
            )

        return ms

    def __get_perfil(self, metrics: list[Metrics]) -> str:
        m = max(metrics, key=lambda x: x.interactions)
        for desc in self.labels:
            for k, v in desc.items():
                if k in self.get_place_by_id(m.place_id).name:
                    return v

        return "Formando perfil"

    def __get_music_genre(self, metrics: list[Metrics]) -> str:
        m = max(metrics, key=lambda x: x.interactions)
        for desc in self.genres:
            for k, v in desc.items():
                if k in self.get_place_by_id(m.place_id).name:
                    return v

        return "Eclético"

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

        user_data.perfil = self.__get_perfil(user_data.metrics)

    def get_all_places(self) -> Iterable[Place]:
        return self.places

    def get_place_by_id(self, place_id) -> Place:
        for place in self.places:
            if place.place_id == place_id:
                return place
        return None

    def like_place(self, place_id):
        place = self.get_place_by_id(place_id)
        place.likes += 1
        return place
