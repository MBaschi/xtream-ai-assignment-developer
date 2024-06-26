import sqlite3
import json
import pandas as pd
from flask import Blueprint, request
from flask import jsonify
from app.utils import load_model, get_model_pickle_path
from setting import DEFAULT_DATASET, DB_PATH
from models.utils import (
    load_df,
    data_cleaning,
)

api_bp = Blueprint("api", __name__)


@api_bp.after_request
def after_request_for_api_hystory_storage(response):
    """
    Logs API request details to the SQLite database after each request.

    This function is executed after each API request. It connects to an SQLite
    database specified by the DB_PATH variable, and inserts the details of the
    API request and response into the api_history table. This includes the API
    endpoint (path), the request payload, and the response data.

    Parameters:
    - response: The response object that is about to be sent to the client.

    Returns:
    - The unmodified response object, ensuring that the logging operation does
      not interfere with the response sent back to the client.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert the new model's details
    cursor.execute(
        """
            INSERT INTO api_history (api, request, response)
            VALUES (?, ?, ?)
        """,
        (request.path, json.dumps(request.json), json.dumps(response.json)),
    )

    # Commit and close
    conn.commit()
    conn.close()
    return response


@api_bp.route("/predict_price")
def predict_diamond_price():
    """
    Predict the price of a diamond based on its characteristics.

    This endpoint accepts JSON input containing the characteristics of a diamond,
    the name of the model, and the model version to use for prediction. It returns
    the predicted price of the diamond.

    The input JSON should have the following format:
    {
        "data": {
            "carat": "value",
            "cut": "text",
            "color": "text",
            "clarity": "text",
            "depth": "value",
            "table": "value",
            "x": "value",
            "y": "value",
            "z": "value"
        },
        "model_name": "model_name_here",
        "model_version": "model_version_here"
    }

    Returns:
        JSON response containing the predicted price or an error message.
    """
    input_data = request.json.get("data")
    model_name = request.json.get("model_name")
    model_version = request.json.get("model_version")

    # TODO add check for data correctness
    #     check if all columns are present in the input data
    #     check if the data types are correct
    #     check if the data is in the correct range
    #     check if the data is not empty
    #     check if the model name exist
    #     check if the model version exist

    path = get_model_pickle_path(model_name, model_version)
    model = load_model(path)

    input_data = pd.DataFrame(input_data)
    input_data = data_cleaning(input_data, target_present=False)

    if len(input_data) == 0:
        return jsonify({"error": "Invalid input data"}), 400

    prediction = model.execution_pipeline(input_data)
    return jsonify({"result": prediction.tolist()})


@api_bp.route("/similar_diamonds")
def find_similar_diamonds():
    """
    Find diamonds with similar characteristics to the input diamond.

    This endpoint accepts JSON input containing the characteristics of a diamond
    and the number of similar diamonds to find. It returns a list of similar diamonds
    based on the specified characteristics.

    The input JSON should have the following format:
    {
        "data": {
            "carat": "value",
            "cut": "text",
            "color": "text",
            "clarity": "text",
            "depth": "value",
            "table": "value",
            "x": "value",
            "y": "value",
            "z": "value"
        },
        "num_similar_diamonds": integer_value
    }

    Returns:
        JSON response containing a list of similar diamonds or an error message.
    """

    input_data = request.json.get("data")
    num_similar_diamonds = request.json.get("num_similar_diamonds")

    data = load_df(DEFAULT_DATASET)
    input_data = pd.DataFrame(input_data)
    input_data = data_cleaning(input_data, target_present=False)
    if len(input_data) == 0:
        return jsonify({"error": "Invalid input data"}), 400

    data_same_characteristics = data.loc[
        (data["cut"] == input_data["cut"].values[0])
        & (data["color"] == input_data["color"].values[0])
        & (data["clarity"] == input_data["clarity"].values[0])
    ].copy()  # Make a copy to avoid SettingWithCopyWarning

    data_same_characteristics["carat difference"] = (
        data_same_characteristics["carat"] - input_data["carat"].values[0]
    ).abs()
    data_same_characteristics.sort_values("carat difference", inplace=True)
    if len(data_same_characteristics) <= num_similar_diamonds:
        return jsonify({"result": data_same_characteristics.values.tolist()})
    else:
        return jsonify(
            {
                "result": data_same_characteristics.iloc[
                    :num_similar_diamonds
                ].values.tolist()
            }
        )
