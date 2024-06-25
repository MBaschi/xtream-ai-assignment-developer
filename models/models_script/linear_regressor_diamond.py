import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from models.base_model import BaseSupervisedModel
from sklearn.preprocessing import OneHotEncoder


class LinearRegressorModelDiamond(BaseSupervisedModel):
    """Linear Regressor model for the diamond dataset."""

    model = LinearRegression()
    model_name = "Linear Regressor"
    model_description = "Predicting the value of diamons base on they carapteristics with linear regression"
    metrics = {"r2": [], "mae": []}

    ohe = OneHotEncoder(drop="first")

    def input_preprocessing(self, x: pd.DataFrame) -> np.array:
        # Dropping unnecessary columns
        x_numeric = x.drop(
            columns=["cut", "color", "clarity", "depth", "table", "y", "z"]
        )

        # Selecting only the categorical columns for one-hot encoding
        x_categorical = x[["cut", "color", "clarity"]]

        # Fitting the OneHotEncoder and transforming the categorical data
        # Check if the encoder has been fitted
        if not hasattr(self.ohe, "categories_"):
            self.ohe=self.ohe.fit(x_categorical)
        x_encoded = self.ohe.transform(x_categorical).toarray()

        # Concatenating the numeric and encoded categorical data
        x_preprocessed = np.hstack((x_numeric.values, x_encoded))

        return x_preprocessed

    @staticmethod
    def target_preprocessing(y:np.array) -> np.array:
        return np.log(y)

    def fit(self, x, y):
        self.model.fit(x, y)
        return self.model

    def evaluate(self, y_predicted, y_real):
        r2 = r2_score(y_real, y_predicted)
        mae = mean_absolute_error(y_real, y_predicted)
        self.metrics["r2"] = r2
        self.metrics["mae"] = mae
        return self.metrics

    def predict(self, x):
        return self.model.predict(x)

    @staticmethod
    def postprocessing(y:np.array) -> np.array:
        return np.exp(y)
