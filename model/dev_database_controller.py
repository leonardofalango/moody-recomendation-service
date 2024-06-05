from typing import Iterable
from model.types import UserData


class DevDatabaseController:
    def __init__(self) -> None:
        self.user_data = {
            "1": {
                "user_id": "1",
                "age": 20,
                "music_genre": "Rock",
                "metrics": [
                    {"label": "Bar de Rock", "interactions": 8},
                    {"label": "Sambô", "interactions": 2},
                    {"label": "Rjota", "interactions": 1},
                    {"label": "Rock Pizza Roll", "interactions": 5},
                    {"label": "Hard Rock Café", "interactions": 5},
                ],
            },
            "2": {
                "user_id": "2",
                "age": 20,
                "music_genre": "Pagode",
                "metrics": [
                    {"label": "Sambô", "interactions": 14},
                    {"label": "Rjota", "interactions": 15},
                    {"label": "Bar de Rock", "interactions": 2},
                ],
            },
            "3": {
                "user_id": "3",
                "age": 20,
                "music_genre": "Funk",
                "metrics": [
                    {"label": "Bar de Rock", "interactions": 1},
                    {"label": "Sambô", "interactions": 2},
                    {"label": "Rjota", "interactions": 1},
                    {"label": "+55", "interactions": 20},
                    {"label": "Lvl Clube", "interactions": 8},
                ],
            },
            "4": {
                "user_id": "4",
                "age": 20,
                "music_genre": "Rock",
                "metrics": [],
            },
            "5": {
                "user_id": "5",
                "age": 20,
                "music_genre": "Funk",
                "metrics": [],
            },
        }

    def get_all(self) -> Iterable[UserData]:
        return self.user_data
