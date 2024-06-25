import pandas as pd
import xgboost
import optuna
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from models.base_model import BaseSupervisedModel


class XgBoostDiamond(BaseSupervisedModel):
    """Linear Regressor model for the diamond dataset."""

    model = xgboost.XGBRegressor(enable_categorical=True, random_state=42)
    model_name = "XgBoost"
    model_description = (
        "Predicting the value of diamons base on they carapteristics with xgboost"
    )
    metrics = {"r2": [], "mae": []}

    @staticmethod
    def input_preprocessing(x: pd.DataFrame) -> pd.DataFrame:
        x["cut"] = pd.Categorical(
            x["cut"],
            categories=["Fair", "Good", "Very Good", "Ideal", "Premium"],
            ordered=True,
        )
        x["color"] = pd.Categorical(
            x["color"], categories=["D", "E", "F", "G", "H", "I", "J"], ordered=True
        )
        x["clarity"] = pd.Categorical(
            x["clarity"],
            categories=["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"],
            ordered=True,
        )
        return x

    @staticmethod
    def target_preprocessing(y: pd.DataFrame) -> pd.DataFrame:
        return y

    def fit(self, x: pd.DataFrame, y: pd.DataFrame):
        best_params = self.optimize_hyperparam(x, y)
        self.model = xgboost.XGBRegressor(
            **best_params, enable_categorical=True, random_state=42
        )
        self.model.fit(x, y)
        return self.model

    def evaluate(self, y_predicted: pd.DataFrame, y_real: pd.DataFrame):
        r2 = r2_score(y_real, y_predicted)
        mae = mean_absolute_error(y_real, y_predicted)
        self.metrics["r2"] = r2
        self.metrics["mae"] = mae
        return self.metrics

    def predict(self, x: pd.DataFrame):
        return self.model.predict(x)

    @staticmethod
    def postprocessing(y: pd.DataFrame):
        return y

    @staticmethod
    def optimize_hyperparam(x: pd.DataFrame, y: pd.DataFrame) -> None:

        def objective(trial: optuna.trial.Trial) -> float:
            # Define hyperparameters to tune
            param = {
                "lambda": trial.suggest_float("lambda", 1e-8, 1.0, log=True),
                "alpha": trial.suggest_float("alpha", 1e-8, 1.0, log=True),
                "colsample_bytree": trial.suggest_categorical(
                    "colsample_bytree", [0.3, 0.4, 0.5, 0.7]
                ),
                "subsample": trial.suggest_categorical(
                    "subsample", [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
                ),
                "learning_rate": trial.suggest_float(
                    "learning_rate", 1e-8, 1.0, log=True
                ),
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
                "max_depth": trial.suggest_int("max_depth", 3, 9),
                "random_state": 42,
                "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
                "enable_categorical": True,
            }

            # Split the training data into training and validation sets
            x_train, x_val, y_train, y_val = train_test_split(
                x, y, test_size=0.2, random_state=42
            )

            # Train the model
            model = xgboost.XGBRegressor(**param)
            model.fit(x_train, y_train)

            # Make predictions
            preds = model.predict(x_val)

            # Calculate MAE
            mae = mean_absolute_error(y_val, preds)

            return mae

        study = optuna.create_study(direction="minimize", study_name="Diamonds XGBoost")
        study.optimize(objective, n_trials=100)
        return study.best_params
