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
