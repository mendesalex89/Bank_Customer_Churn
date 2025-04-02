"""
Configuration module for the project.
Contains all the necessary settings and paths.
"""
from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "Bank Customer Churn Prediction.csv"
MODELS_PATH = PROJECT_ROOT / "models"
REPORTS_PATH = PROJECT_ROOT / "reports"

# Data configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.25

# Feature groups
NUMERIC_FEATURES = [
    'credit_score',
    'age',
    'tenure',
    'balance',
    'products_number',
    'estimated_salary'
]

CATEGORICAL_FEATURES = [
    'country',
    'gender',
    'credit_card',
    'active_member'
]

TARGET = 'churn'

# Model parameters
MODEL_PARAMS = {
    'lightgbm': {
        'objective': 'binary',
        'metric': 'auc',
        'verbose': -1
    },
    'xgboost': {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'silent': 1
    }
}

# API settings
API_TITLE = "Bank Customer Churn Prediction API"
API_DESCRIPTION = "API for predicting customer churn probability"
API_VERSION = "1.0.0" 