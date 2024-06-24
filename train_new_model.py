"""In the following code, will be implemented the pipeline for training the model with new data """

from models.utils import (
    load_df,
    data_cleaning,
)
from models.get_model import get_model
from setting import TRAINING_DATASET, DEFAULT_ALGORITHM


def train_new_model(dataset_path:str ,model_name:str = DEFAULT_ALGORITHM)-> None:
    """Main function to train the model with the diamond dataset."""

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
    model.save_model(training_dataset_name= dataset_path.stem)


if __name__ == "__main__":
    train_new_model(TRAINING_DATASET, model_name = 'linear_regression')
