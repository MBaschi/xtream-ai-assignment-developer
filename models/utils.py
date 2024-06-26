"""In this file are implemented the loading and processing of the diamond dataset"""

import pandas as pd


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


def data_cleaning(df: pd.DataFrame, target_present: bool = True) -> pd.DataFrame:
    """
    Clean the DataFrame by removing missing values, zero dimensions, and negative prices.

    Parameters:
    - df (pd.DataFrame): The DataFrame to clean.
    - target_present (bool): Whether the target column is present in the DataFrame.
        if data_cleaning is done on new data (without target column), set it to False

    Returns:
    - pd.DataFrame: The cleaned DataFrame.
    """
    df = df.dropna()
    df = df[(df[["x", "y", "z"]] != 0).all(axis=1)]
    if target_present:
        df = df[df.price > 0]
    return df
