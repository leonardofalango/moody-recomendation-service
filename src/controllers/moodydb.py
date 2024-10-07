from collections import defaultdict
from typing import Dict
import psycopg2
from dotenv import load_dotenv
import os
from src.types.basic_types import User, Place, Metrics, FavoritePlaces
import logging

logger = logging.getLogger("app_logger")
load_dotenv()


class PostgressController:
    def __init__(self):
        logger.info("Connecting to the database.")
        self.connection = psycopg2.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_NAME"),
        )
        self.cursor = self.connection.cursor()

        self.user_props = (
            "u.id, u.name, u.email, u.role, u.age, u.music_genre, u.gender"
        )

        self.place_props = "l.id, l.slug, l.name, l.rating, l.price_level"
        self.metrics_props = "id, userId, tagsId, interest, label"

    def get_all_users(self) -> list[User]:
        self.cursor.execute(f"""SELECT {self.user_props} FROM users u""")
        all_users = self.cursor.fetchall()

        user_ids = [user[0] for user in all_users]

        # Lazy loading
        metrics = self.get_all_metrics(user_ids)
        favorites = self.get_all_favorites(user_ids)

        return [
            User(
                user_id=user[0],
                name=user[1],
                age=user[4],
                music_genre=user[5],
                gender=user[6],
                metrics=metrics.get(user[0], []),
                favorite_places=favorites.get(user[0], []),
            )
            for user in all_users
        ]

    def get_all_metrics(self, user_ids: list[str]) -> Dict[str, list[Metrics]]:
        self.cursor.execute(
            f"""
            SELECT um.id, um."userId", til."local_id", um."tagsId", um.interest, t.label
            FROM user_metrics um
            INNER JOIN tags t ON um."tagsId" = t.id
            INNER JOIN tags_in_locals til ON t.id = til."tag_id"
            WHERE um."userId" = ANY(%s)
            """,
            (user_ids,),
        )
        metrics = self.cursor.fetchall()

        metrics_by_user = defaultdict(list)
        for metric in metrics:
            metrics_by_user[metric[1]].append(
                Metrics(
                    place_id=metric[2],
                    user_id=metric[1],
                    interactions=metric[4],
                    interest=metric[5],
                )
            )
        return metrics_by_user

    def get_all_favorites(self, user_ids: list[str]) -> Dict[str, list[FavoritePlaces]]:
        self.cursor.execute(
            """
            SELECT local_id, user_id
            FROM locals_favorites 
            WHERE user_id = ANY(%s)
            """,
            (user_ids,),
        )
        favorites = self.cursor.fetchall()

        favorites_by_user = defaultdict(list)
        for favorite in favorites:
            favorites_by_user[favorite[1]].append(
                FavoritePlaces(place_id=favorite[0], user_id=favorite[1])
            )
        return favorites_by_user

    def get_user_by_id(self, user_id: str) -> User:
        self.cursor.execute(
            f"""SELECT {self.user_props} FROM users u WHERE u.id = %s""",
            (user_id,),
        )
        user = self.cursor.fetchone()

        if not user:
            logger.warning("User not found.")
            return None

        return User(
            user_id=user[0],
            name=user[1],
            metrics=self.get_user_metrics(user[0]),
            age=user[4],
            music_genre=user[5],
            gender=user[6],
            favorite_places=self.get_user_favorite_places(user[0]),
        )

    def get_user_metrics(self, user_id: str) -> list[Metrics]:
        self.cursor.execute(
            f"""
            SELECT um.id, um."userId", til."local_id", um."tagsId", um.interest, t.label
            FROM user_metrics um
            INNER JOIN tags t ON um."tagsId" = t.id
            INNER JOIN tags_in_locals til ON t.id = til."tag_id"
            WHERE um."userId" = %s
            """,
            (user_id,),
        )
        user_metrics = self.cursor.fetchall()
        m = [
            Metrics(
                place_id=metric[2],
                user_id=metric[1],
                interactions=metric[4],
                interest=metric[5],
            )
            for metric in user_metrics
        ]
        return m

    def get_user_favorite_places(self, user_id: str) -> list[FavoritePlaces]:
        self.cursor.execute(
            """
            SELECT local_id, user_id
            FROM locals_favorites 
            WHERE user_id = %s
            """,
            (user_id,),
        )
        favorites = self.cursor.fetchall()

        return [
            FavoritePlaces(place_id=favorite[0], user_id=favorite[1])
            for favorite in favorites
        ]

    def get_all_places(self) -> list[Place]:
        self.cursor.execute(f"""SELECT {self.place_props} FROM locals l""")
        all_places = self.cursor.fetchall()
        return [
            Place(
                place_id=place[0],
                likes=self.get_place_likes(place[0]),
                slug=place[1],
            )
            for place in all_places
        ]

    def get_top_places(self, start: int, limit: int) -> list[Place]:
        self.cursor.execute(
            f"""SELECT {self.place_props} FROM locals l ORDER BY l.rating DESC LIMIT %s OFFSET %s""",
            (limit, start),
        )
        top_places = self.cursor.fetchall()
        return [
            Place(
                place_id=place[0],
                likes=self.get_place_likes(place[0]),
                slug=place[1],
            )
            for place in top_places
        ]

    def get_place_by_id(self, place_id: str) -> Place:
        self.cursor.execute(
            f"""SELECT {self.place_props} FROM locals l WHERE l.id = %s""",
            (place_id,),
        )

        place = self.cursor.fetchone()
        if not place:
            logger.warning("Place not found.")
            return None

        return Place(
            place_id=place[0], likes=self.get_place_likes(place[0]), slug=place[1]
        )

    def get_place_likes(self, place_id: str) -> int:
        self.cursor.execute(
            """SELECT COUNT(*) FROM locals_likes WHERE local_id = %s""", (place_id,)
        )
        likes = self.cursor.fetchone()[0]
        return likes

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        logger.info("Database connection closed.")

    def get_user_page(self, page: int, items_per_page: int) -> list[User]:
        self.cursor.execute(
            f"""SELECT {self.user_props} FROM users u LIMIT %s OFFSET %s""",
            (items_per_page, page),
        )
        users = self.cursor.fetchall()
        return [
            User(
                user_id=user[0],
                name=user[1],
                age=user[4],
                music_genre=user[5],
                gender=user[6],
                metrics=self.get_user_metrics(user[0]),
                favorite_places=self.get_user_favorite_places(user[0]),
            )
            for user in users
        ]


if __name__ == "__main__":
    db = PostgressController()
    print(db.get_all_users())
    print(db.get_all_places())
    db.close_connection()
