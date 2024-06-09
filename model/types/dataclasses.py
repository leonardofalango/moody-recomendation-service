import dataclasses
from pydantic import BaseModel
from typing import Protocol, Iterable


class Metrics(BaseModel):
    label: str
    interactions: int


class User(BaseModel):
    user_id: str
    age: int
    music_genre: str
    metrics: list[Metrics] | None


class RatePlace(BaseModel):
    user_id: str
    label: str
    interactions: int


class DatabaseController(Protocol):
    def create(obj) -> None: ...
    def find(user_id: str) -> User: ...
    def delete(user_id: str) -> User: ...
    def update(data: User, where: User | str): ...
    def get_all() -> Iterable[User]: ...
