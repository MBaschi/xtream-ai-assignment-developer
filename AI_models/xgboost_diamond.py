from sklearn.linear_model import LinearRegression
from AI_models.base_model import BaseSupervisedModel


class XgBoostDiamond(BaseSupervisedModel):
    """Linear Regressor model for the diamond dataset."""

    def __init__(self):
        self.model = LinearRegression
        self.model_name = "Linear Regressor"
        self.model_description = "Linear Regressor is a linear approach to modeling the relationship between a scalar response (or dependent variable) and one or more explanatory variables (or independent variables)."
        self.metrics = {"r2": [], "mae": []}

    def input_preprocessing(self, x):
        pass

    def target_preprocessing(self, y):
        pass

    def fit(self, x, y):
        pass

    def evaluate(self, y_predicted, y_real):
        pass

    def predict(self, x):
        pass

    def postprocessing(self, y):
        pass
