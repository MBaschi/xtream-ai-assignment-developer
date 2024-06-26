import os
import shutil
import sqlite3
import cloudpickle
from setting import DB_PATH,SAVE_PATH_MODELS


def get_model_pickle_path(model_name, model_version=None):
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if model_version:
        # Retrieve the pickle_path for the given model_name and model_version
        cursor.execute(
            """
            SELECT model_pickle_path
            FROM models_history 
            WHERE model_name = ? AND model_version = ?
            """,
            (model_name, model_version),
        )
    else:
        # Retrieve the pickle_path for the given model_name with the maximum version
        cursor.execute(
            """
            SELECT model_pickle_path
            FROM models_history 
            WHERE model_name = ? AND model_version = (
                SELECT MAX(model_version) 
                FROM models_history 
                WHERE model_name = ?
            )
            """,
            (model_name, model_name),
        )
    pickle_path = cursor.fetchone()
    conn.close()
    return pickle_path[0]


def load_model(model_path: str):
    """Load the model from the given path."""
    with open(model_path, "rb") as file:
        model = cloudpickle.load(file)
    return model

def delete_all_models_pickle_file():
    folder = SAVE_PATH_MODELS
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
