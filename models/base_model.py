"""In the following file is present the BaseModel class that will be used 
as parent for all the models that will be implemented in the project."""

from abc import ABC, abstractmethod
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from sklearn.model_selection import train_test_split
import numpy as np


class BaseSupervisedModel(ABC):

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Returns the name of the model."""

    @property
    @abstractmethod
    def model_description(self) -> str:
        """Returns a description of the model."""

    @property
    @abstractmethod
    def metrics(self) -> dict:
        """Returns a dictionary containing the evaluation metrics of the model."""

    @abstractmethod
    def input_preprocessing(self, x):
        """
        Preprocesses the input data before feeding it to the model.

        Parameters:
            x: The input data to be preprocessed.

        Returns:
            The preprocessed input data.
        """

    @abstractmethod
    def target_preprocessing(self, y):
        """
        Preprocesses the target data before model training or evaluation.

        Parameters:
            y: The target data to be preprocessed.

        Returns:
            The preprocessed target data.
        """

    @abstractmethod
    def fit(self, x, y):
        """
        Trains the model on the given data.

        Parameters:
            x: The preprocessed input data.
            y: The preprocessed target data.
        """

    @abstractmethod
    def evaluate(self, y_predicted, y_real):
        """
        Evaluates the model's performance on the test data.

        Parameters:
            y_predicted: The model's predictions.
            y_real: The actual target values.

        Returns:
            A dictionary containing the evaluation metrics.
        """

    @abstractmethod
    def predict(self, x):
        """
        Generates predictions for the given input data.

        Parameters:
            x: The preprocessed input data.

        Returns:
            The predicted values.
        """

    @abstractmethod
    def postprocessing(self, y):
        """
        Postprocesses the model's predictions or the target data.

        Parameters:
            y: The data to be postprocessed (either predictions or target).

        Returns:
            The postprocessed data.
        """

    def train_test_split(self, x, y, test_size, seed=np.random.randint(0, 2**16 - 1)):
        """
        Splits the data into training and testing sets.

        Parameters:
            x: The input data.
            y: The target data.
            test_size: The proportion of the dataset to include in the test split.
            seed: The seed for the random number generator.

        Returns:
            The split data: x_train, x_test, y_train, y_test.
        """
        return train_test_split(x, y, test_size=test_size, random_state=seed)

    def train_pipeline(self, x, y, print_final_metrics=False):
        """
        Executes the complete training pipeline including preprocessing, splitting,
        training, predicting, postprocessing, and evaluating.

        Parameters:
            x: The input data as a pandas DataFrame.
            y: The target data as a pandas DataFrame.
            print_final_metrics: print the final metrics of the process

        Returns:
            The evaluation metrics as a numpy array.
        """
        x = self.input_preprocessing(x)
        y = self.target_preprocessing(y)
        x_train, x_test, y_train, y_test = self.train_test_split(x, y, test_size=0.2)
        self.fit(x_train, y_train)
        y_pred = self.predict(x_test)
        y_pred = self.postprocessing(y_pred)
        y_test = self.postprocessing(y_test)
        self.metrics = self.evaluate(y_pred, y_test)
        if print_final_metrics:
            for metric in self.metrics:
                print(f"{metric}: {self.metrics[metric]}")

    def execution_pipeline(self, x):
        """
        Executes the prediction pipeline including preprocessing, predicting,
        and postprocessing.

        Parameters:
            x: The input data.

        Returns:
            The postprocessed predictions.
        """
        x = self.input_preprocessing(x)
        y_pred = self.predict(x)
        y_pred = self.postprocessing(y_pred)
        return y_pred

    def save_model_anagraphic(self, path: str, training_dataset_name: str) -> None:
        try:
            with open(path, "r") as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []

        # Append the new model's details to the history list
        history.append(
            {
                "Model": self.model_name,
                "Version": len(history) + 1,
                "Dataset": training_dataset_name,
                "Metrics": self.metrics,
                "Creation date": datetime.now(tz=ZoneInfo("UTC")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

        # Write the updated history back to the file
        with open(path, "w") as f:
            f.write(json.dumps(history, indent=4))
            print("Model saved ")