"""This module provides functionality to retrieve specific model instances.

It defines a function `get_model` that returns an instance of a model based on 
the provided model name.
"""

import models


def get_model(model_name: str):
    """Retrieve a model instance based on the model name.

    Args:
    model_name (str): The name of the model to retrieve.

    Returns:
    models.BaseModel: An instance of the requested model.

    Raises:
    ValueError: If the specified model name does not match any supported models.
    """
    if model_name == models.LinearRegressorModelDiamond().model_name:
        return models.LinearRegressorModelDiamond()
    elif model_name == models.XgBoostDiamond().model_name:
        return models.XgBoostDiamond()
    else:
        raise ValueError("Model not supported")
