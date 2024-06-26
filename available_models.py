"""In the following code, will be implemented the pipeline for training the model with new data """
import os
import argparse
from setting import SAVE_PATH_MODELS, DB_PATH
import sqlite3

def print_exixting_model(model) -> None:
    # Assuming SAVE_PATH_MODELS is the directory you want to list files from
    for filename in os.listdir(SAVE_PATH_MODELS):
        filepath = os.path.join(SAVE_PATH_MODELS, filename)
        if os.path.isfile(filepath):
            print(filepath)



    # Connect to the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Calculate the new version number for this model
    cursor.execute(
        "SELECT model_pickle_path FROM models_history WHERE model_name = ?",
        (model,),
    )
    print(f"\n path :{cursor.fetchone()[0]}")
    # Commit and close
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a new model with the specified dataset."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="XgBoost",
        help="The file path to the dataset used for training.",
    )
    args = parser.parse_args()
    print_exixting_model(args.model)
