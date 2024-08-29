import psycopg2
from dotenv import load_dotenv
import os
from src.types.basic_types import User, Place, Metrics
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

        return [
            User(
                user_id=user[0],
                name=user[1],
                age=user[4],
                music_genre=user[5],
                gender=user[6],
                metrics=self.get_user_metrics(user[0]),
            )
            for user in all_users
        ]

    def get_user_by_id(self, user_id: str) -> User:
        self.cursor.execute(
            f"""SELECT {self.user_props} FROM users u WHERE u.id = %s""",
            (user_id,),
        )
        user = self.cursor.fetchone()
        return User(
            user_id=user[0],
            name=user[1],
            metrics=self.get_user_metrics(user[0]),
            age=user[4],
            music_genre=user[5],
            gender=user[6],
        )

    def get_user_metrics(self, user_id: str) -> list[Metrics]:
        self.cursor.execute(
            f"""
            SELECT um.id, um."userId", um."tagsId", um.interest, t.label
            FROM user_metrics um
            INNER JOIN tags t ON um."tagsId" = t.id
            WHERE um."userId" = %s
            """,
            (user_id,),
        )
        user_metrics = self.cursor.fetchall()
        return [
            Metrics(
                place_id=metric[2],
                user_id=metric[1],
                interactions=metric[3],
            )
            for metric in user_metrics
        ]

    def get_all_places(self) -> list[Place]:
        self.cursor.execute(f"""SELECT {self.place_props} FROM locals l""")
        all_places = self.cursor.fetchall()
        return [
            Place(
                place_id=place[0],
                likes=self.get_place_likes(place[0]),
            )
            for place in all_places
        ]

    def get_place_by_id(self, place_id: str) -> Place:
        logger.debug(f"Query: SELECT {self.place_props} FROM locals l WHERE l.id = %s")
        logger.debug(f"Parameters: {place_id}")
        self.cursor.execute(
            f"""SELECT {self.place_props} FROM locals l WHERE l.id = %s""",
            (place_id,),
        )

        place = self.cursor.fetchone()
        if not place:
            logger.warning("Place not found.")
            return None

        return Place(
            place_id=place[0],
            likes=self.get_place_likes(place[0]),
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


if __name__ == "__main__":
    db = PostgressController()
    print(db.get_all_users())
    print(db.get_all_places())
    db.close_connection()
