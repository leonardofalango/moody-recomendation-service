from pydantic import BaseModel
from typing import Protocol, Iterable


class Place(BaseModel):
    place_id: str
    likes: int


class PlaceDTO(BaseModel):
    place_id: str
    score: float | None = 0.0


class Metrics(BaseModel):
    place_id: str
    user_id: str
    interactions: int
    interest: str | None


class User(BaseModel):
    user_id: str
    name: str
    age: int
    gender: str
    music_genre: str
    perfil: str = "Formando perfil..."
    metrics: list[Metrics] | None


class Interaction(BaseModel):
    user_id: str
    place_id: str
    interactions: int


class Label(BaseModel):
    label: str
    description: str


class DatabaseController(Protocol):
    def create(obj) -> None: ...
    def find(user_id: str) -> User: ...
    def delete(user_id: str) -> User: ...
    def update(data: User, where: User | str): ...
    def get_all() -> Iterable[User]: ...
