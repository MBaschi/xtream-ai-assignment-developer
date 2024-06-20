"""In this file are implemented the loading and processing of the diamond dataset"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def load_df(path: str) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file.

    Parameters:
    - path (str): The file path to the CSV file.

    Returns:
    - pd.DataFrame: The loaded DataFrame.
    """
    df = pd.read_csv(path)
    return df


def preprocess_diamond_return_train_and_test_set(df: pd.DataFrame) -> tuple:
    """
    Preprocess the DataFrame and split it into training and testing sets.

    The function performs data cleaning, data preparation, and then splits the data
    into training and testing sets with a test size of 20% and a fixed random state
    for reproducibility.

    Parameters:
    - df (pd.DataFrame): The DataFrame to preprocess.

    Returns:
    - tuple: A tuple containing the training and testing sets (x_train, x_test, y_train, y_test).
    """
    data = data_cleaning(df)
    x, y = data_preparation(data)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    y_train_log = np.log(y_train)
    return x_train, x_test, y_train_log, y_test


def data_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by removing missing values, zero dimensions, and negative prices.

    Parameters:
    - df (pd.DataFrame): The DataFrame to clean.

    Returns:
    - pd.DataFrame: The cleaned DataFrame.
    """
    df = df.dropna()
    df = df[(df[["x", "y", "z"]] != 0).all(axis=1)]
    df = df[df.price > 0]
    return df


def data_preparation(df: pd.DataFrame) -> tuple:
    """
    Prepare the DataFrame for modeling by removing non-useful features, applying one-hot encoding,
    and setting input and target variables.

    Parameters:
    - df (pd.DataFrame): The DataFrame to prepare.

    Returns:
    - tuple: A tuple containing the input features (x) and the target variable (y).
    """
    df = df.drop(columns=["depth", "table", "y", "z"])
    df = pd.get_dummies(df, columns=["cut", "color", "clarity"], drop_first=True)
    x = df.drop(columns="price")
    y = df.price
    return x, y

def postprocessing(y: np.array) -> np.array:
    """
    Postprocess the DataFrame by adding a new column with the predicted prices.

    Parameters:
    - df (pd.DataFrame): The DataFrame to postprocess.

    Returns:
    - pd.DataFrame: The postprocessed DataFrame.
    """
    y_postprocessed = np.exp(y)
    return y_postprocessed
