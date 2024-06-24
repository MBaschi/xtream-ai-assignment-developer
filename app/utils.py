import cloudpickle
import sqlite3
from setting import DB_PATH
def get_last_model_version_pickle_path(model_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Calculate the new version number for this model
    cursor.execute(
        "SELECT MAX(model_version) FROM models_history WHERE model_name = ?",
        (model_name),
    )
    max_version = cursor.fetchone()[0]
    new_version = 1 if max_version is None else max_version + 1


def load_model(model_path: str):
    """Load the model from the given path."""
    with open(model_path,"rb") as file:
        model = cloudpickle.load(file)
    return model

