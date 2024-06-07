import json
import random
import pathlib
from typing import Iterable
from model.types import UserData


class DevDatabaseController:
    def __init__(self, population: int = 100) -> None:
        self.user_data = {}
        self.genres = [
            "Rock",
            "Pop",
            "Hip Hop",
            "Electronic",
            "Jazz",
            "Funk",
            "Reggae",
            "Blues",
            "R&B",
            "Country",
            "Classical",
            "Soul",
            "Metal",
            "Indie",
            "Alternative",
            "EDM",
            "Disco",
            "Ska",
            "Punk",
            "Trap",
        ]

        path = pathlib.Path("./")
        self.metrics = json.load(open(path / "model" / "data" / "metrics.json"))[
            "metrics"
        ]
        self.max_places = int(len(self.metrics) / 2)
        self.max_interactions = int(self.max_places / 4)

        for i in range(population):
            self.user_data[str(i)] = self.__generate_fake_data(i)

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
        return self.user_data

    def get_by_id(self, user_id: str) -> UserData:
        return self.user_data[user_id]
