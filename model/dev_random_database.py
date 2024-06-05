import random
from typing import Iterable
from model.types import UserData


class DevDatabaseController:
    def __init__(self, population: int = 100) -> None:
        self.user_data = {}
        for i in range(population):
            self.user_data[str(i)] = self.__generate_fake_data(i)

    def __generate_fake_data(self, user_id):
        age = random.randint(18, 19)
        music_genre = random.choice(
            ["Rock", "Pop", "Hip Hop", "Electronic", "Jazz", "Funk", "Reggae"]
        )
        metrics = [
            {"label": "Geekbar"},
            {"label": "Another Geekbar"},
            {"label": "Rock-and-Roll bar"},
            {"label": "Shovel"},
            {"label": "Palladium"},
            {"label": "Shopping"},
            {"label": "Ice-Cream Shop"},
            {"label": "Eiffel Tower"},
            {"label": "Bariguas Park"},
            {"label": "Blue Lake Agua Park"},
        ]

        return {
            "user_id": str(user_id),
            "age": age,
            "music_genre": music_genre,
            "metrics": [
                dict(random.choice(metrics), interactions=random.randint(0, 10))
                for x in range(random.randint(0, 20))
            ],
        }

    def get_all(self) -> Iterable[UserData]:
        return self.user_data
