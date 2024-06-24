import models as models


def get_model(model_name):
    if model_name == models.LinearRegressorModelDiamond().model_name:
        return models.LinearRegressorModelDiamond()
    elif model_name == models.XgBoostDiamond().model_name:
        return models.XgBoostDiamond()
    else:
        raise ValueError("Model not supported")
