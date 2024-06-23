import AI_models as models

def get_model(model_name):
    if model_name == "linear_regression":
        return models.LinearRegressorModelDiamond()
    elif model_name == "xgboost":
        return models.XgBoostDiamond()
    else:
        raise ValueError("Model not supported")