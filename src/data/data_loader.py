"""
Module for loading and validating the dataset.
"""
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from src.utils.config import (
    CATEGORICAL_FEATURES,
    DATA_PATH,
    NUMERIC_FEATURES,
    RANDOM_STATE,
    TARGET,
    TEST_SIZE,
)


def load_data() -> pd.DataFrame:
    """
    Load the raw dataset from the csv file.
    
    Returns:
        pd.DataFrame: Raw dataset
    """
    return pd.read_csv(DATA_PATH)


def validate_data(df: pd.DataFrame) -> bool:
    """
    Validate the dataset structure and contents.
    
    Args:
        df (pd.DataFrame): Dataset to validate
        
    Returns:
        bool: True if validation passes, raises exception otherwise
    """
    # Check required columns
    required_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET]
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Check data types
    numeric_dtypes = df[NUMERIC_FEATURES].dtypes
    if not all(dtype.kind in 'iuf' for dtype in numeric_dtypes):
        raise ValueError("Invalid data type in numeric features")
    
    # Check target values
    if not set(df[TARGET].unique()).issubset({0, 1}):
        raise ValueError("Target column contains invalid values")
    
    return True


def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the dataset into training and testing sets.
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        Tuple containing:
        - X_train (pd.DataFrame): Training features
        - X_test (pd.DataFrame): Testing features
        - y_train (pd.Series): Training target
        - y_test (pd.Series): Testing target
    """
    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = df[features]
    y = df[TARGET]
    
    return train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    ) 