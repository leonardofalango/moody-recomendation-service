from model.dev_database_controller import DevDatabaseController
from typing import List, Dict


class CustomRecommendationModel:
    def __init__(self, db_controller: DevDatabaseController):
        self.db_controller = db_controller
        self.user_data = db_controller.get_all()

    def recommend(self, user_id: str) -> List[str]:
        user_info = self.user_data.get(user_id)
        if not user_info:
            return []

        user_interactions = [metric["label"] for metric in user_info["metrics"]]

        similar_users = self.find_similar_users(user_info)

        recommendations = self.aggregate_recommendations(similar_users)

        recommendations = [
            item for item in recommendations if item not in user_interactions
        ]

        return recommendations

    def find_similar_users(self, user_info: Dict) -> List[Dict]:
        similar_users = []
        for user_id, data in self.user_data.items():
            if user_id != user_info["user_id"]:
                if (
                    data["age"] == user_info["age"]
                    and data["music_gente"] == user_info["music_gente"]
                ):
                    similar_users.append(data)
        return similar_users

    def aggregate_recommendations(
        self, similar_users: List[Dict], k: int = 5
    ) -> List[str]:
        recommendations = {}
        for user in similar_users:
            for metric in user["metrics"]:
                label = metric["label"]
                interactions = metric["interactions"]
                if label not in recommendations:
                    recommendations[label] = 0
                recommendations[label] += interactions
        sorted_recommendations = sorted(
            recommendations, key=recommendations.get, reverse=True
        )
        return sorted_recommendations[:5]


if __name__ == "__main__":
    import sys

    db_controller = DevDatabaseController()
    recommendation_model = CustomRecommendationModel(db_controller)
    user_id = sys.argv[1]
    recommendations = recommendation_model.recommend(user_id)
    print("Recomendações para o usuário", user_id, ":", recommendations)
