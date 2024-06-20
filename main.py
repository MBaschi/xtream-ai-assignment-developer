"""In the following code, will be implemented the pipeline for training the model with new data """

import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from data_processing import (
    load_df,
    preprocess_diamond_return_train_and_test_set,
    postprocessing,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

ROOT_PATH = Path(__file__).resolve().parents[0]
DATA_PATH = ROOT_PATH / "data" / "diamonds.csv"
SAVE_PATH = ROOT_PATH / "model_history.json"


def main():
    """Main function to train the model with the diamond dataset."""

    dataset_name = Path(DATA_PATH).stem
    print(f"Training model with dataset: {dataset_name}")
    # Load the data
    data = load_df(DATA_PATH)
    print("Data loaded \n Preprocessing data...")

    # Preprocess the data
    x_train, x_test, y_train_log, y_test = preprocess_diamond_return_train_and_test_set(
        data
    )
    print("Data Preprocessed \n Training model...")

    # Train the model
    reg = LinearRegression()
    reg.fit(x_train, y_train_log)
    pred = postprocessing(reg.predict(x_test))

    # Evaluate the model
    r2 = r2_score(y_test, pred)
    mae = mean_absolute_error(y_test, pred)
    print(f"Model trained with r2: {r2} and mae: {mae}")

    # Save the model anagraphycs
    try:
        with open(SAVE_PATH, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    # Append the new model's details to the history list
    history.append(
        {
            "Version": len(history) + 1,
            "Dataset": dataset_name,
            "r2": r2,
            "mae": mae,
            "Creation date": datetime.now(tz=ZoneInfo("UTC")).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
    )

    # Write the updated history back to the file
    with open(SAVE_PATH, "w") as f:
        f.write(json.dumps(history, indent=4))

    print(f"Model saved to {SAVE_PATH}")


if __name__ == "__main__":
    main()
