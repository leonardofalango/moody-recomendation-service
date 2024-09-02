import os
import logging
import threading
import numpy as np
from typing import List, Dict, Optional
from collections import defaultdict
from src.types.repository import Repository
from src.types.basic_types import User, PlaceDTO

logger = logging.getLogger("app_logger")

weights = {
    "metrics": 0.65,
    "age": 0.05,
    "music_genre": 0.15,
    "gender": 0.05,
    "tags": 0.1,
}


class CustomRecommendationModel:
    def __init__(self, db_controller: Repository):
        logger.info("Initializing recommendation model")
        self.db_controller = db_controller
        self.user_data = self._load_user_data()
        self.user_cache = {}
        self.recommendation_cache = {}

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
    ) -> List[PlaceDTO]:
        logger.info("Recommending to user %s", user_id)
        user_info = self.db_controller.get_user_by_id(user_id)

        if not user_info:
            logger.warning("User not found")
            return []

        start_index = page * items_per_page
        end_index = start_index + items_per_page

        similar_users = self.user_cache.get(user_id)

        if not similar_users:
            similar_users = self.find_similar_users(user_info, k_neighboors)
            self.user_cache[user_id] = similar_users

        recommendations = self.recommendation_cache.get(user_id)
        if not recommendations:
            recommendations = self.aggregate_recommendations(similar_users)
            self.recommendation_cache[user_id] = recommendations

        recommendations_slice = recommendations[start_index:end_index]
        recommendations_slice_result = []

        for place_id in recommendations_slice:
            place = self.db_controller.get_place_by_id(place_id)
            if not place:
                logger.warning("Place not found: %s", place_id)
                continue
            recommendations_slice_result.append(
                PlaceDTO(place_id=place.place_id, slug=place.slug)
            )

        # fill the remaining items with top places
        if len(recommendations_slice_result) < items_per_page:
            remaining_items = items_per_page - len(recommendations_slice_result)
            offset = start_index + len(recommendations_slice_result)
            additional_places = self._get_top_places(offset, remaining_items, user_info)
            logger.warning(
                "Filling recommendations with top places, params, %s, %s",
                offset,
                remaining_items,
            )
            recommendations_slice_result.extend(additional_places)

        for place in recommendations_slice_result:
            place.score = self._calculate_average_similarity(
                user_info, similar_users, k_neighboors, place.place_id
            )

        return recommendations_slice_result

    def find_similar_users(self, user_info: User, k: int = 10) -> List[User]:
        logger.debug("Finding similar users")
        similar_users = [
            (data, self.calculate_similarity(user_info, data))
            for user_id, data in self.user_data.items()
            if user_id != user_info.user_id
        ]
        similar_users = [u for u in similar_users if u[1] > self.similarity_min]
        similar_users.sort(key=lambda x: x[1], reverse=True)

        logger.debug(
            "Found %s similar users for user %s", len(similar_users), user_info.user_id
        )
        return similar_users[:k]

    def calculate_similarity(self, user1: User, user2: User) -> float:
        metrics1 = {metric.place_id: metric.interactions for metric in user1.metrics}
        metrics2 = {metric.place_id: metric.interactions for metric in user2.metrics}

        common_metrics = set(metrics1.keys()).intersection(metrics2.keys())

        if common_metrics:
            vec1 = np.array([metrics1[metric] for metric in common_metrics])
            vec2 = np.array([metrics2[metric] for metric in common_metrics])
            norm_vec = np.linalg.norm(vec1) * np.linalg.norm(vec2)
            metrics_similarity = np.dot(vec1, vec2) / norm_vec if norm_vec > 0 else 0.0
        else:
            metrics_similarity = 0.0

        max_age_difference = 100
        age_similarity = 1 - abs(user1.age - user2.age) / max_age_difference

        similarities = {
            "metrics": metrics_similarity,
            "age": age_similarity,
            "music_genre": 1.0 if user1.music_genre == user2.music_genre else 0.0,
            "gender": 1.0 if user1.gender == user2.gender else 0.0,
            "tags": self._calculate_tag_similarity(user1, user2),
        }

        overall_similarity = sum(
            similarities[key] * weights[key] for key in similarities
        )
        return overall_similarity

    def aggregate_recommendations(self, similar_users: List[User]) -> List[str]:
        logger.debug("Aggregating recommendations")
        recommendations = defaultdict(int)

        for user, similarity in similar_users:
            for metric in user.metrics:
                recommendations[metric.place_id] += metric.interactions

        sorted_recommendations = sorted(
            recommendations, key=recommendations.get, reverse=True
        )
        logger.debug("Found %s recommendations", len(sorted_recommendations))
        return sorted_recommendations

    def clear_cache(self, user_id: Optional[str] = None):
        logger.info("Clearing cache")
        if user_id is None:
            self.user_cache.clear()
            self.recommendation_cache.clear()
        else:
            self.user_cache.pop(user_id, None)
            self.recommendation_cache.pop(user_id, None)

    def _load_user_data(self) -> Dict[str, User]:
        logger.debug("Loading user data")
        user_data = {}
        for user in self.db_controller.get_all_users():
            try:
                user_data[user.user_id] = user
            except Exception as e:
                logger.error("Error loading user data: %s", str(user))
        return user_data

    def _get_top_places(self, start: int, limit: int, user: User) -> List[PlaceDTO]:
        logger.debug("Getting top places")
        places = self.db_controller.get_top_places(start=start, limit=limit)
        places.sort(key=lambda x: x.likes, reverse=True)
        # sort by user interest
        user_metrics = {metric.place_id: metric.interactions for metric in user.metrics}
        sorted_places = sorted(
            places,
            key=lambda x: user_metrics.get(x.place_id, 0),
            reverse=True,
        )

        return [
            PlaceDTO(place_id=place.place_id, slug=place.slug)
            for place in sorted_places
        ]

    def _calculate_average_similarity(
        self,
        user_info: User,
        similar_users: List[User],
        k_neighboors: int,
        place_id: str,
    ) -> float:
        total_similarity = 0.0
        total_weight = 0.0

        for user, similarity in similar_users:
            user_metrics = {
                metric.place_id: metric.interactions for metric in user.metrics
            }
            if place_id in user_metrics:
                interaction_weight = user_metrics[place_id]
                total_similarity += similarity * interaction_weight
                total_weight += interaction_weight

        if total_weight == 0:
            return 0.0
        return total_similarity / total_weight

    def _calculate_tag_similarity(self, user1: User, user2: User) -> float:
        tags1 = {metric.interest for metric in user1.metrics}
        tags2 = {metric.interest for metric in user2.metrics}

        common_tags = tags1.intersection(tags2)
        all_tags = tags1.union(tags2)

        if all_tags:
            return len(common_tags) / len(all_tags)
        return 0.0

    def recommend_all_users(self):
        logger.info("Recommending to all users in background")
        background_thread = threading.Thread(
            target=self._recommend_all_users_in_background
        )
        background_thread.start()

    def _recommend_all_users_in_background(self):
        for user in self.db_controller.get_all_users():
            self.recommend(user.user_id)
