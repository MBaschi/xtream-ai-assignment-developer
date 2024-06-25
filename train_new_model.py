"""In the following code, will be implemented the pipeline for training the model with new data """

import argparse
from models.utils import (
    load_df,
    data_cleaning,
)
from models.get_model import get_model
from setting import DEFAULT_DATASET, DEFAULT_ALGORITHM


def train_new_model(dataset_path: str, model_name: str = DEFAULT_ALGORITHM) -> None:
    """Trains a new model using the specified dataset.

    This function orchestrates the process of training a model by first loading and
    cleaning the dataset, then separating it into features and target variable.
    It subsequently retrieves the specified model, trains it using the prepared data,
    finally saves the trained model.

    Args:
        dataset_path (str): The file path to the dataset used for training.
        model_name (str, optional): The name of the algorithm to use for training.
            Defaults to DEFAULT_ALGORITHM.
    """

    # Load the data
    data = load_df(dataset_path)
    # Clean the data
    data = data_cleaning(data)
    # Select input and target data
    x = data.drop(columns=["price"])
    y = data["price"]

    # Get the model
    model = get_model(model_name)
    model.train_pipeline(x, y, print_final_metrics=True)
    model.save_model(training_dataset_name=dataset_path.stem)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a new model with the specified dataset."
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default=DEFAULT_DATASET,
        help="The file path to the dataset used for training.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_ALGORITHM,
        help="""The name of the algorithm to use for training. Available options:
        'Linear Regressor', 'XgBoost'
        """,
    )

    args = parser.parse_args()

    train_new_model(args.dataset, model_name=args.model)
