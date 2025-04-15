import pytest
import numpy as np
import pandas as pd
from src.model.predictor import ChurnPredictor

@pytest.fixture
def sample_input():
    return {
        "CreditScore": 619,
        "Geography": "France",
        "Gender": "Female",
        "Age": 42,
        "Tenure": 2,
        "Balance": 0.0,
        "NumOfProducts": 1,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 101348.88
    }

@pytest.fixture
def churn_predictor():
    return ChurnPredictor()

def test_prediction_format(churn_predictor, sample_input):
    """Test if prediction returns the correct format"""
    result = churn_predictor.predict(sample_input)
    
    assert isinstance(result, dict)
    assert "churn_probability" in result
    assert "is_likely_to_churn" in result
    assert "risk_level" in result
    
    assert isinstance(result["churn_probability"], float)
    assert isinstance(result["is_likely_to_churn"], bool)
    assert result["risk_level"] in ["Low", "Medium", "High"]

def test_prediction_range(churn_predictor, sample_input):
    """Test if prediction probability is between 0 and 1"""
    result = churn_predictor.predict(sample_input)
    assert 0 <= result["churn_probability"] <= 1

def test_risk_level_thresholds(churn_predictor):
    """Test risk level classification thresholds"""
    test_cases = [
        (0.1, "Low"),
        (0.4, "Medium"),
        (0.8, "High")
    ]
    
    for prob, expected in test_cases:
        risk_level = churn_predictor.get_risk_level(prob)
        assert risk_level == expected

def test_input_validation(churn_predictor):
    """Test input validation"""
    invalid_input = {
        "CreditScore": "invalid",  # Should be integer
        "Geography": "Brazil",     # Invalid country
        "Age": -1                  # Invalid age
    }
    
    with pytest.raises(ValueError):
        churn_predictor.validate_input(invalid_input)

def test_feature_preprocessing(churn_predictor, sample_input):
    """Test feature preprocessing"""
    processed = churn_predictor.preprocess_features(pd.DataFrame([sample_input]))
    
    assert isinstance(processed, pd.DataFrame)
    assert all(processed.notna().all())
    assert processed.shape[1] == len(sample_input)

def test_batch_prediction(churn_predictor):
    """Test batch prediction functionality"""
    batch_input = [
        {
            "CreditScore": 619,
            "Geography": "France",
            "Gender": "Female",
            "Age": 42,
            "Tenure": 2,
            "Balance": 0.0,
            "NumOfProducts": 1,
            "HasCrCard": 1,
            "IsActiveMember": 1,
            "EstimatedSalary": 101348.88
        },
        {
            "CreditScore": 700,
            "Geography": "Germany",
            "Gender": "Male",
            "Age": 35,
            "Tenure": 5,
            "Balance": 50000.0,
            "NumOfProducts": 2,
            "HasCrCard": 1,
            "IsActiveMember": 1,
            "EstimatedSalary": 120000.0
        }
    ]
    
    results = churn_predictor.predict_batch(batch_input)
    
    assert isinstance(results, list)
    assert len(results) == len(batch_input)
    for result in results:
        assert "churn_probability" in result
        assert "is_likely_to_churn" in result
        assert "risk_level" in result 