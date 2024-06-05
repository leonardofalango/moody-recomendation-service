from model.dev_database_controller import DevDatabaseController

database_controller = DevDatabaseController()

user_data = database_controller.get_all()
print(user_data.get("1"))
