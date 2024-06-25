import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from models.base_model import BaseSupervisedModel



class LinearRegressorModelDiamond(BaseSupervisedModel):
    """Linear Regressor model for the diamond dataset."""

    model = LinearRegression()
    model_name = "Linear Regressor"
    model_description = "Predicting the value of diamons base on they carapteristics with linear regression"
    metrics = {"r2": [], "mae": []}

    @staticmethod
    def input_preprocessing(x: pd.DataFrame) -> np.array:
        x.drop(columns=["depth", "table", "y", "z"], inplace=True)
        x = pd.get_dummies(x, columns=["cut", "color", "clarity"], drop_first=True)
        return x.values

    @staticmethod
    def target_preprocessing(y):
        return np.log(y)

    def fit(self, x, y):
        self.model.fit(x, y)
        
    def evaluate(self, y_predicted, y_real):
        r2 = r2_score(y_real, y_predicted)
        mae = mean_absolute_error(y_real, y_predicted)
        self.metrics["r2"] = r2
        self.metrics["mae"] = mae
        return self.metrics

    def predict(self, x):
        return self.model.predict(x)

    @staticmethod
    def postprocessing(y):
        return np.exp(y)
