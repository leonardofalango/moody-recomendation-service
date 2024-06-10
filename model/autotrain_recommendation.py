import numpy as np
from typing import List
from model.types.basic_types import User
from model.types.repository import Repository
from custom_recommendation_model import CustomRecommendationModel


class AutoTrainedCustomRecommendation(CustomRecommendationModel):
    def __init__(self, db_controller: Repository):
        self.weights = {"metrics": 0.33, "age": 0.33, "music_genre": 0.33}
        self.boolean_features = ["music_genre", ...]
        self.float_features = ["age", ...]

    def optimize_weights(self, validation_data: List[User]) -> None:
        best_score = 0
        best_weights = self.weights.copy()

        features = list(self.weights.keys())

        num_features = len(features)

        for i in range(num_features):
            for w in np.linspace(0, 1, num=11):
                new_weights = self.weights.copy()
                new_weights[features[i]] = w
                remaining_weight = (1 - w) / (num_features - 1)
                for j in range(num_features):
                    if j != i:
                        new_weights[features[j]] = remaining_weight

                self.weights = new_weights

                score = self.evaluate_model(validation_data)

                if score > best_score:
                    best_score = score
                    best_weights = new_weights.copy()

        self.weights = best_weights

    def evaluate_model(self, validation_data: List[User]) -> float:
        total_users = len(validation_data)
        total_correct_recommendations = 0

        for user_info in validation_data:
            user_id = user_info.user_id
            actual_interactions = set(metric.place_id for metric in user_info.metrics)

            recommendations = self.recommend(user_id)
            recommended_items = set(recommendations)

            intersection = recommended_items.intersection(actual_interactions)

            precision = (
                len(intersection) / len(recommended_items) if recommended_items else 0
            )

            total_correct_recommendations += precision

        avg_precision = (
            total_correct_recommendations / total_users if total_users else 0
        )

        # ? Implement other metrics such as f1 recall and more.
        return avg_precision

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

        metrics_value = self.weights["metrics"] * metrics_similarity
        return metrics_value + self._calc_overall_similarity_debug(user1, user2)

    def _calc_overall_similarity_debug(self, user1: User, user2: User):
        similarities_value = {}

        overrall_similarity = 0

        for feature, value in self.weights.items():
            if feature in self.boolean_features:
                similarities_value[feature] = (
                    1.0 if getattr(user1, feature) == getattr(user2, feature) else 0
                )

            elif feature in self.float_features:
                similarities_value[feature] = 1 - (
                    getattr(user1, feature) - getattr(user2, feature) / 100
                )

        for k in similarities_value.keys():
            overrall_similarity += similarities_value[k] * self.weights[k]

        return overrall_similarity

    def _calc_overall_similarity(self, user1: User, user2: User):
        overrall_similarity = 0

        for feature, weight in self.weights.items():
            if feature in self.boolean_features:
                overrall_similarity += weight * (
                    1.0 if getattr(user1, feature) == getattr(user2, feature) else 0
                )

            elif feature in self.float_features:
                overrall_similarity = weight * 1 - (
                    getattr(user1, feature) - getattr(user2, feature) / 100
                )

        return overrall_similarity
