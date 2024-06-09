import numpy as np
from sklearn.linear_model import LinearRegression

training_data = [
    # {"user1": user1, "user2": user2, "similarity": 0.8},
]

X = []
y = []

for data in training_data:
    user1, user2, true_similarity = data["user1"], data["user2"], data["similarity"]

    metrics1 = {metric["label"]: metric["interactions"] for metric in user1["metrics"]}
    metrics2 = {metric["label"]: metric["interactions"] for metric in user2["metrics"]}
    common_metrics = set(metrics1.keys()).intersection(set(metrics2.keys()))

    if common_metrics:
        vec1 = np.array([metrics1[metric] for metric in common_metrics])
        vec2 = np.array([metrics2[metric] for metric in common_metrics])
        norm_vec = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        metrics_similarity = np.dot(vec1, vec2) / norm_vec if norm_vec > 0 else 0.0
    else:
        metrics_similarity = 0.0

    max_age_difference = 100
    age_difference = abs(user1["age"] - user2["age"])
    age_similarity = 1 - (age_difference / max_age_difference)

    genre_similarity = 1.0 if user1["music_genre"] == user2["music_genre"] else 0.0

    X.append([metrics_similarity, age_similarity, genre_similarity])
    y.append(true_similarity)

model = LinearRegression().fit(X, y)
weights = model.coef_

weight_metrics, weight_age, weight_genre = weights
