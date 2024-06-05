from typing import Iterable
from model.types import UserData


class DevDatabaseController:
    def __init__(self) -> None:
        self.user_data = {
            "1": {
                "user_id": "1",
                "age": 20,
                "music_gente": "Rock",
                "metrics": [
                    {"user_id": "1", "label": "Bar de Rock", "interactions": 8},
                    {"user_id": "1", "label": "Sambô", "interactions": 2},
                    {"user_id": "1", "label": "Rjota", "interactions": 1},
                    {"user_id": "1", "label": "Rock Pizza Roll", "interactions": 5},
                    {"user_id": "1", "label": "Hard Rock Café", "interactions": 5},
                ],
            },
            "2": {
                "user_id": "2",
                "age": 20,
                "music_gente": "Pagode",
                "metrics": [
                    {"user_id": "2", "label": "Sambô", "interactions": 14},
                    {"user_id": "2", "label": "Rjota", "interactions": 15},
                    {"user_id": "2", "label": "Bar de Rock", "interactions": 2},
                ],
            },
            "3": {
                "user_id": "3",
                "age": 20,
                "music_gente": "Funk",
                "metrics": [
                    {"user_id": "3", "label": "Bar de Rock", "interactions": 1},
                    {"user_id": "3", "label": "Sambô", "interactions": 2},
                    {"user_id": "3", "label": "Rjota", "interactions": 1},
                    {"user_id": "3", "label": "+55", "interactions": 20},
                    {"user_id": "3", "label": "Lvl Clube", "interactions": 8},
                ],
            },
            "4": {
                "user_id": "4",
                "age": 20,
                "music_gente": "Rock",
                "metrics": [],
            },
            "5": {
                "user_id": "5",
                "age": 20,
                "music_gente": "Funk",
                "metrics": [],
            },
        }

    def get_all(self) -> Iterable[UserData]:
        return self.user_data
