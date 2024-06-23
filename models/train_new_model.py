"""In the following code, will be implemented the pipeline for training the model with new data """

import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from models.utils import (
    load_df,
    data_cleaning,
)
from models.get_model import get_model

ROOT_PATH = Path(__file__).resolve().parents[0]
DATA_PATH = ROOT_PATH / "data" / "diamonds.csv"
SAVE_PATH = ROOT_PATH / "model_history.json"
MODEL_NAME = "xgboost"


def main():
    """Main function to train the model with the diamond dataset."""

    # Load the data
    data = load_df(DATA_PATH)
    # Clean the data
    data = data_cleaning(data)
    # Select input and target data
    x = data.drop(columns=["price"])
    y = data["price"]

    # Get the model
    model = get_model(MODEL_NAME)
    model.train_pipeline(x, y, print_final_metrics=True)
    model.save_model_anagraphic(
        path=SAVE_PATH, training_dataset_name=Path(DATA_PATH).stem
    )


if __name__ == "__main__":
    main()
