import pandas as pd
from flask import Blueprint, request
from app.utils import load_model, get_model_pickle_path
from flask import jsonify
from setting import TRAINING_DATASET
from models.utils import (
    load_df,
    data_cleaning,
)

api_bp = Blueprint("api", __name__)


@api_bp.route("/predict_price")
def predict_diamond_price():

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
    input_data = data_cleaning(input_data)
    if len(input_data) == 0:
        return jsonify({"error": "Invalid input data"}), 400

    prediction = model.execution_pipeline(input_data)
    return jsonify({"message": prediction})


@api_bp.route("/similar_diamonds")
def find_similar_diamonds():

    input_data = request.json.get("input_data")
    num_similar_diamonds = request.json.get("num_similar_diamonds")

    data = load_df(TRAINING_DATASET)
    input_data = pd.DataFrame(input_data)
    input_data = data_cleaning(input_data)
    if len(input_data) == 0:
        return jsonify({"error": "Invalid input data"}), 400

    data_same_carteristics = data[
        data["cut"] == input_data["cut"],
        data["color"] == input_data["color"],
        data["clarity"] == input_data["clarity"],
    ]
    data_same_carteristics["carat difference"] = (
        data_same_carteristics["carat"] - input_data["carat"]
    )
    data_same_carteristics.sort_values("carat difference", inplace=True)
    if len(data_same_carteristics) <= num_similar_diamonds:
        return jsonify({"message": data_same_carteristics})
    else:
        return jsonify({"message": data_same_carteristics.loc[:num_similar_diamonds]})
