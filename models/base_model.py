"""In the following file is present the BaseModel class that will be used 
as parent for all the models that will be implemented in the project."""

from abc import ABC, abstractmethod
import json
from datetime import datetime, timezone
import sqlite3
from sklearn.model_selection import train_test_split
import numpy as np
import cloudpickle
from setting import DB_PATH, SAVE_PATH_MODELS
import os 

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

    @property
    @abstractmethod
    def model(self):
        """Returns the model instance."""

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
        Returns:
            self.model: the fitted model
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
        self.model = self.fit(x_train, y_train)
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

    def save_model_pickle(self, path: str) -> None:
        """Save the model in a pickle file."""
        with open(path, "wb") as f:
            cloudpickle.dump(self, f)
            print("Model saved ")

    def save_model(self, training_dataset_name: str) -> None:
        """Save the model in the database and as pickle file."""

        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Calculate the new version number for this model
        cursor.execute(
            "SELECT MAX(model_version) FROM models_history WHERE model_name = ?",
            (self.model_name,),
        )
        max_version = cursor.fetchone()[0]
        new_version = 1 if max_version is None else max_version + 1

        pickle_path = os.path.join(SAVE_PATH_MODELS,self.model_name + str(new_version) + ".pkl")
        # Insert the new model's details
        cursor.execute(
            """
            INSERT INTO models_history (model_name, model_version, training_dataset, metrics, 
            created, model_description,model_pickle_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                self.model_name,
                new_version,
                training_dataset_name,
                json.dumps(self.metrics),
                datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                self.model_description,
                pickle_path,
            ),
        )
        self.save_model_pickle(path=pickle_path)

        # Commit and close
        conn.commit()
        conn.close()
