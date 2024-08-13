import sqlite3
import logging
from typing import Iterable
from dotenv import load_dotenv
from src.types.repository import Repository
from src.types.basic_types import User, Interaction, Metrics, Place, Label

logger = logging.getLogger("app_logger")
load_dotenv()


class SqliteController(Repository):
    def __init__(self, db_name: str = "database.db") -> None:
        logger.info("Database initiating")
        self.db_name = db_name
        self._connect()
        self.__generate_tables()
        logger.info("Database initiated")
        logger.info("Database loaded with %s data", len(self.get_all_users()))

    def __del__(self):
        self._disconnect()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn.isolation_level = None  # Set to None to use autocommit mode

    def _disconnect(self):
        self.conn.close()

    def __generate_tables(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id TEXT PRIMARY KEY,
                age INTEGER,
                music_genre TEXT,
                perfil TEXT,
                FOREIGN KEY (user_id) REFERENCES metrics(user_id)
            )
            """
            )
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS metrics (
                user_id TEXT,
                place_id TEXT,
                interactions INTEGER,
                PRIMARY KEY (user_id, place_id)
            )
            """
            )
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS places (
                place_id TEXT PRIMARY KEY,
                name TEXT,
                location TEXT,
                rating REAL,
                likes INTEGER,
                image TEXT
            )
            """
            )
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS labels (
                label TEXT PRIMARY KEY,
                description TEXT
            )
            """
            )
            self.conn.commit()

    def __get_perfil(self, metrics: list[Metrics]) -> str:
        m = max(metrics, key=lambda x: x.interactions)
        for desc in self.get_all_labels():
            if desc.label == m.place_id:
                return desc.description
        return "Formando perfil"

    #! USERS
    def get_all_users(self) -> Iterable[User]:
        logger.info("Getting all users")
        users = []
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            users_data = cursor.fetchall()
            for data in users_data:
                user_id, age, music_genre, perfil = data
                cursor.execute("SELECT * FROM metrics WHERE user_id = ?", (user_id,))
                metrics_data = cursor.fetchall()
                metrics = [
                    Metrics(user_id=row[0], place_id=row[1], interactions=row[2])
                    for row in metrics_data
                ]
                users.append(
                    User(
                        user_id=user_id,
                        age=age,
                        music_genre=music_genre,
                        perfil=perfil,
                        metrics=metrics,
                    )
                )
        logger.info("Returning %s users", len(users))
        return users

    def get_page(self, quantity: int = 500, off_set: int = 0) -> Iterable[User]:
        logger.info("Getting %s users skipping %s", quantity, off_set)
        users = []
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM usuarios LIMIT ? OFFSET ?", (quantity, off_set)
            )
            users_data = cursor.fetchall()
            for data in users_data:
                user_id, age, music_genre, perfil = data
                cursor.execute("SELECT * FROM metrics WHERE user_id = ?", (user_id,))
                metrics_data = cursor.fetchall()
                metrics = [
                    Metrics(user_id=row[0], place_id=row[1], interactions=row[2])
                    for row in metrics_data
                ]
                users.append(
                    User(
                        user_id=user_id,
                        age=age,
                        music_genre=music_genre,
                        perfil=perfil,
                        metrics=metrics,
                    )
                )
        return users

    def create_user(self, data: User) -> None:
        logger.info("Creating user data")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO usuarios (user_id, age, music_genre, perfil) VALUES (?, ?, ?, ?)
            """,
                (data.user_id, data.age, data.music_genre, data.perfil),
            )
            for metric in data.metrics:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO metrics (user_id, place_id, interactions) VALUES (?, ?, ?)
                """,
                    (metric.user_id, metric.place_id, metric.interactions),
                )
            self.conn.commit()

    def get_user_by_id(self, user_id: str) -> User:
        logger.info("Getting user from database")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                user_id, age, music_genre, perfil = user_data
                cursor.execute("SELECT * FROM metrics WHERE user_id = ?", (user_id,))
                metrics_data = cursor.fetchall()
                metrics = [
                    Metrics(user_id=row[0], place_id=row[1], interactions=row[2])
                    for row in metrics_data
                ]
                user = User(
                    user_id=user_id,
                    age=age,
                    music_genre=music_genre,
                    perfil=perfil,
                    metrics=metrics,
                )
                return user
        return None

    def update_user(self, user_id: str, data: User) -> None:
        logger.info("Updating user data")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE usuarios SET age = ?, music_genre = ?, perfil = ? WHERE user_id = ?
            """,
                (data.age, data.music_genre, data.perfil, user_id),
            )
            cursor.execute("DELETE FROM metrics WHERE user_id = ?", (user_id,))
            for metric in data.metrics:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO metrics (user_id, place_id, interactions) VALUES (?, ?, ?)
                """,
                    (metric.user_id, metric.place_id, metric.interactions),
                )
            self.conn.commit()

    def delete_user(self, user_id: str) -> None:
        logger.info("Deleting user data")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM metrics WHERE user_id = ?", (user_id,))
            self.conn.commit()

    #! PLACES
    def get_all_places(self) -> Iterable[Place]:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM places")
            places_data = cursor.fetchall()
            places = [
                Place(
                    place_id=row[0],
                    name=row[1],
                    location=row[2],
                    rating=row[3],
                    likes=row[4],
                    image=row[5],
                )
                for row in places_data
            ]
        return places

    def create_place(self, place: Place) -> None:
        logger.info("Creating place data")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO places (place_id, name, location, rating, likes, image) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    place.place_id,
                    place.name,
                    place.location,
                    place.rating,
                    place.likes,
                    place.image,
                ),
            )
            self.conn.commit()

    def get_place_by_id(self, place_id) -> Place:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM places WHERE place_id = ?", (place_id,))
            place_data = cursor.fetchone()
            if place_data:
                place = Place(
                    place_id=place_data[0],
                    name=place_data[1],
                    location=place_data[2],
                    rating=place_data[3],
                    likes=place_data[4],
                    image=place_data[5],
                )
                return place
        return None

    def update_place(self, place_id: str, place: Place) -> None:
        logger.info("Updating place data")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE places SET name = ?, location = ?, rating = ?, likes = ?, image = ? WHERE place_id = ?
            """,
                (
                    place.name,
                    place.location,
                    place.rating,
                    place.likes,
                    place.image,
                    place_id,
                ),
            )
            self.conn.commit()

    def delete_place(self, place_id: str) -> None:
        logger.info("Deleting place data")
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM places WHERE place_id = ?", (place_id,))
            self.conn.commit()

    def interact(self, rate_place: Interaction) -> None:
        logger.info("Interaction with a place")
        user = self.get_user_by_id(rate_place.user_id)
        if user:
            for metric in user.metrics:
                if metric.place_id == rate_place.place_id:
                    metric.interactions += rate_place.interactions
                    break
            else:
                user.metrics.append(
                    Metrics(
                        user_id=rate_place.user_id,
                        place_id=rate_place.place_id,
                        interactions=rate_place.interactions,
                    )
                )
            self.update_user(rate_place.user_id, user)
