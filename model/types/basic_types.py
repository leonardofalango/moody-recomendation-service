from pydantic import BaseModel
from typing import Protocol, Iterable


class Place(BaseModel):
    place_id: str
    name: str
    location: str
    rating: float
    likes: int
    image: str


class Metrics(BaseModel):
    place_id: str
    user_id: str
    interactions: int


class User(BaseModel):
    user_id: str
    age: int
    music_genre: str
    perfil: str
    metrics: list[Metrics] | None


class RatePlace(BaseModel):
    user_id: str
    place_id: str
    interactions: int


class DatabaseController(Protocol):
    def create(obj) -> None: ...
    def find(user_id: str) -> User: ...
    def delete(user_id: str) -> User: ...
    def update(data: User, where: User | str): ...
    def get_all() -> Iterable[User]: ...
