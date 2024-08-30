import os
import logging
import threading
import numpy as np
from typing import List
from collections import defaultdict
from src.types.repository import Repository
from src.types.basic_types import User, Place

logger = logging.getLogger("app_logger")

similarities = defaultdict()
weights = {"metrics": 0.7, "age": 0.1, "music_genre": 0.1, "gender": 0.1}


class CustomRecommendationModel:
    def __init__(self, db_controller: Repository):
        logger.info("Initializing recommendation model")
        self.db_controller = db_controller
        self.user_data = self._load_user_data()
        self.user_cache = {}

        self.similarity_min = float(os.environ.get("SIMILARITY", 0.1))

        logger.info("Loaded %s users", len(self.user_data))
        logger.info("Similarity threshold: %s", self.similarity_min)
        logger.info("Recommendation model initialized")

    def recommend(
        self,
        user_id: str,
        page: int = 0,
        items_per_page: int = 5,
        k_neighboors: int = 5,
    ) -> List[Place]:
        logger.info("Recommending to user %s", user_id)
        user_info = self.db_controller.get_user_by_id(user_id)

        if not user_info:
            logger.warning("User not found")
            return []

        if len(user_info.metrics) == 0:
            logger.info("User has no interactions, recommending top places")
            return sorted(
                self.db_controller.get_all_places(),
                key=lambda place: place.likes,
                reverse=True,
            )[page * items_per_page : (page + 1) * items_per_page]

        user_interactions = set(metric.place_id for metric in user_info.metrics)

        if user_id not in self.user_cache:
            similar_users = self.find_similar_users(user_info, k=k_neighboors)
            self.user_cache[user_id] = similar_users
        else:
            similar_users = self.user_cache[user_id]

        recommnedations_for_user = self.aggregate_recommendations(similar_users)

        if len(recommnedations_for_user) < items_per_page:
            recommnedations_for_user += sorted(
                self.db_controller.get_all_places(),
                key=lambda place: place.likes,
                reverse=True,
            )[
                page * items_per_page
                - len(recommnedations_for_user) : (page + 1) * items_per_page
            ]

        return recommnedations_for_user

    def find_similar_users(self, user_info: User, k: int = 10) -> List[User]:
        logger.debug("Finding similar users")

        similar_users = []
        for user_id, data in self.user_data.items():
            if user_id != user_info.user_id:
                similarity = self.calculate_similarity(user_info, data)
                if similarity > self.similarity_min:
                    similar_users.append((data, similarity))

        similar_users.sort(key=lambda x: x[1], reverse=True)
        return [user for user, _ in similar_users[:k]]

    def calculate_similarity(self, user1: User, user2: User) -> float:
        metrics1 = {metric.place_id: metric.interactions for metric in user1.metrics}
        metrics2 = {metric.place_id: metric.interactions for metric in user2.metrics}

        common_metrics = set(metrics1.keys()).intersection(set(metrics2.keys()))

        if not common_metrics:
            metrics_similarity = 0.0
        else:
            vec1 = np.array([metrics1[metric] for metric in common_metrics])
            vec2 = np.array([metrics2[metric] for metric in common_metrics])
            norm_vec = np.linalg.norm(vec1) * np.linalg.norm(vec2)
            metrics_similarity = np.dot(vec1, vec2) / norm_vec if norm_vec > 0 else 0.0

        max_age_difference = 100
        age_difference = abs(user1.age - user2.age)

        similarities["age"] = 1 - (age_difference / max_age_difference)
        similarities["music_genre"] = (
            1.0 if user1.music_genre == user2.music_genre else 0.0
        )
        similarities["gender"] = 1.0 if user1.gender == user2.gender else 0.0
        similarities["metrics"] = metrics_similarity

        overall_similarity = sum(
            similarities[key] * weights[key] for key in similarities.keys()
        )
        return overall_similarity

    def aggregate_recommendations(self, similar_users: List[User]) -> List[str]:
        logger.debug("Aggregating recommendations")
        recommendations = defaultdict(int)
        for user in similar_users:
            for metric in user.metrics:
                place_id = metric.place_id
                interactions = metric.interactions
                recommendations[place_id] += interactions

        sorted_recommendations = sorted(
            recommendations, key=recommendations.get, reverse=True
        )
        logger.debug("Found %s recommendations", len(sorted_recommendations))
        return sorted_recommendations

    def clear_cache(self, user_id: str | None = None):
        logger.info("Clearing cache")
        if user_id is None:
            self.user_cache.clear()
        elif user_id in self.user_cache:
            del self.user_cache[user_id]

    def _load_user_data(self) -> dict[str, User]:
        logger.debug("Loading user data")
        user_data = {}
        for user in self.db_controller.get_all_users():
            try:
                user_data[user.user_id] = user
            except Exception as e:
                logger.error("Error loading user data: %s", str(user))
        return user_data

    def recommend_all_users(self):
        logger.info("Recommending to all users in background")
        background_thread = threading.Thread(
            target=self._recommend_all_users_in_background
        )
        background_thread.start()

    def _recommend_all_users_in_background(self):
        for user in self.db_controller.get_all_users():
            self.recommend(user.user_id)


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    from src.controllers.sqldb import SqliteController

    load_dotenv()

    db_controller = SqliteController()
    recommendation_model = CustomRecommendationModel(db_controller)
    user_id = sys.argv[1]
    recommendations = recommendation_model.recommend(user_id)
    print("Recomendações para o usuário", user_id, ":", recommendations)
