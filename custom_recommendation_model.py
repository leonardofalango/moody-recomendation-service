import os
import logging
import numpy as np
from typing import List
from collections import defaultdict
from model.types.repository import Repository
from model.types.basic_types import User, Place

logger = logging.getLogger("app_logger")


class CustomRecommendationModel:
    def __init__(self, db_controller: Repository):
        logger.info("Initializing recommendation model")
        self.db_controller = db_controller
        self.user_data = self._load_user_data()
        self.user_cache = {}

        self.similarity_min = float(os.environ.get("SIMILARITY", 0.8))

        logger.info("Loaded %s users", len(self.user_data))
        logger.info("Similarity threshold: %s", self.similarity_min)
        logger.info("Recommendation model initialized")

    def recommend(
        self, user_id: str, n_recommendations: int = 20, k_neighboors: int = 5
    ) -> List[Place]:
        logger.info("Recommending to user %s", user_id)
        user_info = self.db_controller.get_by_id(user_id)
        if not user_info:
            logger.info("User not found")
            return []

        if len(user_info.metrics) == 0:
            return sorted(
                self.db_controller.get_all_places(),
                key=lambda place: place["likes"],
                reverse=True,
            )[:n_recommendations]

        user_interactions = set(metric.place_id for metric in user_info.metrics)

        if user_id not in self.user_cache:
            similar_users = self.find_similar_users(user_info, k=k_neighboors)
            self.user_cache[user_id] = similar_users
        else:
            similar_users = self.user_cache[user_id]

        recommendations = self.aggregate_recommendations(
            similar_users, n=n_recommendations + 1
        )
        recommendations = [
            self.db_controller.get_place_by_id(item)
            for item in recommendations
            if item not in user_interactions
        ]

        return recommendations

    def find_similar_users(self, user_info: User, k: int = 10) -> List[User]:
        logger.info("Finding similar users")

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
        age_similarity = 1 - (age_difference / max_age_difference)

        genre_similarity = 1.0 if user1.music_genre == user2.music_genre else 0.0

        weight_metrics = 0.8
        weight_age = 0.1
        weight_genre = 0.1

        overall_similarity = (
            weight_metrics * metrics_similarity
            + weight_age * age_similarity
            + weight_genre * genre_similarity
        )

        return overall_similarity

    def aggregate_recommendations(
        self, similar_users: List[User], n: int = 5
    ) -> List[str]:
        logger.info("Aggregating recommendations")
        recommendations = defaultdict(int)
        for user in similar_users:
            for metric in user.metrics:
                place_id = metric.place_id
                interactions = metric.interactions
                recommendations[place_id] += interactions

        sorted_recommendations = sorted(
            recommendations, key=recommendations.get, reverse=True
        )
        logger.info("Found %s recommendations", len(sorted_recommendations))
        return sorted_recommendations[:n]

    def clear_cache(self, user_id: str | None = None):
        logger.info("Clearing cache")
        if user_id is None:
            self.user_cache.clear()
        elif user_id in self.user_cache:
            del self.user_cache[user_id]

    def _load_user_data(self) -> dict[str, User]:
        logger.info("Loading user data")
        user_data = {}
        for user in self.db_controller.get_all():
            try:
                user_data[user.user_id] = user
            except Exception as e:
                logger.error("Error loading user data: %s", str(user))
        return user_data


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    from model.dev_random_database import DevDatabaseController

    load_dotenv()

    db_controller = DevDatabaseController()
    recommendation_model = CustomRecommendationModel(db_controller)
    user_id = sys.argv[1]
    recommendations = recommendation_model.recommend(user_id)
    print("Recomendações para o usuário", user_id, ":", recommendations)
