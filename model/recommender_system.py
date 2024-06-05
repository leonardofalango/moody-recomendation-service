from typing import Iterable
from model.types import User, UserData
from sklearn.neighbors import NearestNeighbors  # type: ignore
import numpy as np  # type: ignore


class RecommenderSystem:
    def __init__(self, users: Iterable[User], user_data: Iterable[UserData]):
        self.users = {user.user_id: user for user in users}
        self.user_data = {data.user_id: data for data in user_data}
        self.user_matrix = self._prepare_user_matrix()

    def _prepare_user_matrix(self):
        user_features = []
        for user_id, data in self.user_data.items():
            user_features.append(
                [data.age]
            )  # Adicione aqui outras características do usuário, se necessário
        return np.array(user_features)

    def recommend(self, user_id: str, k: int = 2):
        user = self.users.get(user_id)
        if not user:
            return "User not found"
        user_data = self.user_data.get(user_id)
        if not user_data:
            return "UserData not found"

        model_knn = NearestNeighbors(metric="euclidean", algorithm="brute")
        model_knn.fit(self.user_matrix)

        _, indexes = model_knn.kneighbors(
            [self.user_matrix[int(user_id) - 1]], n_neighbors=k + 1
        )

        similar_users = [
            index + 1 for index in indexes.flatten() if index + 1 != int(user_id)
        ]

        similar_users_names = [
            self.users[str(similar_user)].name for similar_user in similar_users
        ]

        return f"Users similar to {user.name}: {', '.join(similar_users_names)}."
