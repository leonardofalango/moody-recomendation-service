import sys
import pickle
from model.types import SklearnModel
from sklearn.neighbors import KNeighborsClassifier  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
from model.dev_database_controller import DevDatabaseController

model: SklearnModel = KNeighborsClassifier(
    n_neighbors=3 if len(sys.argv) >= 0 else sys.argv[1]
)

database_controller = DevDatabaseController
X = database_controller.get_all()

model.fit()
