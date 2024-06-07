from model.dev_random_database import DevDatabaseController


def test_database():
    population = 1_000_000

    database_controller = DevDatabaseController(population)
    user_data = database_controller.get_all()

    assert set(["user_id", "age", "music_genre", "metrics"]) == set(
        user_data["1"].keys()
    )
    assert len(user_data) == population
