import os
import shutil
import sqlite3
import cloudpickle
from setting import DB_PATH, SAVE_PATH_MODELS


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
    if not pickle_path:
        return None
    return pickle_path[0]


def load_model(model_path: str):
    """Load the model from the given path."""
    try:
        with open(model_path, "rb") as file:
            model = cloudpickle.load(file)
    except FileNotFoundError:
        return None
    
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
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def check_data_correctness(input_data_list: dict):
    """
    Validates the correctness of input data based on predefined criteria.

    This function checks if the input data dictionary:
    1. Contains all required columns: 'carat', 'cut', 'color', 'clarity', 'depth', 'table', 'x', 'y', 'z'.
    2. Has string fields ('cut', 'color', 'clarity') with values that match the allowed options.
    3. Has numerical fields ('carat', 'depth', 'table', 'x', 'y', 'z') with values greater than zero.

    Parameters:
    - input_data (dict): A dictionary containing the data to be validated.

    Returns:
    - (bool, str): A tuple where the first element is True if the data is in the correct format, False otherwise.
                   The second element is a message indicating whether the data is correct or describing the error.
    """
    # Define allowed values for string fields
    ALLOWED_CUT = ["Fair", "Good", "Very Good", "Ideal", "Premium"]
    ALLOWED_COLOR = ["D", "E", "F", "G", "H", "I", "J"]
    ALLOWED_CLARITY = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"]

    for input_data in input_data_list:
        # Check if all required columns are present
        required_columns = [
            "carat",
            "cut",
            "color",
            "clarity",
            "depth",
            "table",
            "x",
            "y",
            "z",
        ]
        if not all(column in input_data for column in required_columns):
            return False, "Missing required columns"

        # Check if string fields are of type string and have allowed values
        if (
            not isinstance(input_data["cut"], str)
            or input_data["cut"] not in ALLOWED_CUT
        ):
            return False, "Invalid or incorrect type for 'cut'"
        if (
            not isinstance(input_data["color"], str)
            or input_data["color"] not in ALLOWED_COLOR
        ):
            return False, "Invalid or incorrect type for 'color'"
        if (
            not isinstance(input_data["clarity"], str)
            or input_data["clarity"] not in ALLOWED_CLARITY
        ):
            return False, "Invalid or incorrect type for 'clarity'"

        # Check if numerical fields are greater than zero
        numerical_fields = ["carat", "depth", "table", "x", "y", "z"]
        try:
            if any(float(input_data[field]) <= 0 for field in numerical_fields):
                return False, "Numerical fields must be greater than zero"
        except ValueError:
            return False, "Numerical fields contain non-numeric values"

    # If all checks pass
    return True, "Input data is in the correct format"
