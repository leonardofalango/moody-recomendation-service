import dataclasses
from typing import Protocol, Iterable


class SklearnModel(Protocol):
    def fit(self, X, y, sample_weight=None): ...
    def predict(self, X): ...
    def score(self, X, y, sample_weight=None): ...
    def set_params(self, **params): ...


@dataclasses.dataclass
class User:
    user_id: int
    name: str
    email: str


# @dataclasses.dataclass
# class Place:
#     mood_id: str
#     label: str


@dataclasses.dataclass
class Metrics:
    user_id: str
    label: str
    interactions: int


@dataclasses.dataclass
class UserData:
    user_id: str
    name: str
    age: int
    music_gente: str
    metrics: Iterable[Metrics]


class PredictionModel(Protocol):
    def predict(user_id: str, top: int = 20) -> Iterable[UserData]: ...


class DatabaseController(Protocol):
    def create(obj) -> None: ...
    def find(user_id: str) -> UserData: ...
    def delete(user_id: str) -> User: ...
    def update(data: UserData, where: UserData | str): ...
    def get_all() -> Iterable[UserData]: ...
