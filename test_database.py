from model.dev_database_controller import DevDatabaseController


def test_database():
    database_controller = DevDatabaseController()

    user_data = database_controller.get_all()

    assert set(["user_id", "age", "music_gente", "metrics"]) == set(
        user_data["1"].keys()
    )
