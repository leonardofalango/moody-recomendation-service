from typing import Iterable
from model.types import User, UserData, Metrics


class DevDatabaseController:
    def __init__(self) -> None:
        self._users = {
            "1": User("1", "henrique", "henrique@email.com"),
            "2": User("2", "jorge", "jorge@email.com"),
            "3": User("3", "maria", "maria@email.com"),
            "4": User("4", "madalena", "madalena@email.com"),
            "5": User("5", "jubileu", "jubileu@email.com"),
        }

        self.userData = {
            "1": UserData("1", "henrique", 30, "Bar de Rock and Roll", []),
            "2": UserData("2", "jorge", 30, "Bar de Pop", []),
            "3": UserData("3", "maria", 30, "Bar de Samba", []),
            "4": UserData("4", "madalena", 30, "Bar de Samba", []),
            "5": UserData("5", "jubileu", 30, "Bar de Samba", []),
        }

        self.metrics = [
            Metrics("1", "Bar de Rock and Roll", 8),
            Metrics("1", "Bar de Samba", 2),
            Metrics("1", "Bar de Pop", 1),
            Metrics("2", "Bar de Rock and Roll", 1),
            Metrics("2", "Bar de Samba", 2),
            Metrics("2", "Bar de Pop", 6),
            Metrics("3", "Bar de Rock and Roll", 3),
            Metrics("3", "Bar de Samba", 10),
            Metrics("3", "Bar de Pop", 2),
            Metrics("4", "Bar de Rock and Roll", 1),
            Metrics("4", "Bar de Samba", 4),
            Metrics("4", "Bar de Pop", 1),
            Metrics("5", "Bar de Rock and Roll", 1),
            Metrics("5", "Bar de Samba", 2),
            Metrics("5", "Bar de Pop", 3),
        ]

    def _get_userdata(self, user_id: str) -> UserData:
        self.userData.get(user_id)["metrics"] = self.metrics.get(user_id)

    def get_all(self) -> {Iterable[User], Iterable[UserData]}:
        return self.users, self.userData
