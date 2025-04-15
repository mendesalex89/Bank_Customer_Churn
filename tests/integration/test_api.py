import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint():
    """Test prediction endpoint with valid data"""
    test_input = {
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
    
    response = client.post("/predict", json=test_input)
    assert response.status_code == 200
    
    result = response.json()
    assert "churn_probability" in result
    assert "is_likely_to_churn" in result
    assert "risk_level" in result

def test_predict_invalid_input():
    """Test prediction endpoint with invalid data"""
    invalid_input = {
        "CreditScore": "invalid",
        "Geography": "Invalid",
        "Age": -1
    }
    
    response = client.post("/predict", json=invalid_input)
    assert response.status_code == 422

def test_batch_predict_endpoint():
    """Test batch prediction endpoint"""
    test_input = {
        "customers": [
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
    }
    
    response = client.post("/predict/batch", json=test_input)
    assert response.status_code == 200
    
    results = response.json()["predictions"]
    assert len(results) == len(test_input["customers"])
    
    for result in results:
        assert "churn_probability" in result
        assert "is_likely_to_churn" in result
        assert "risk_level" in result

def test_model_info_endpoint():
    """Test model information endpoint"""
    response = client.get("/model/info")
    assert response.status_code == 200
    
    info = response.json()
    assert "model_version" in info
    assert "performance_metrics" in info
    assert "last_trained" in info

def test_api_authentication():
    """Test API authentication"""
    test_input = {
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
    
    # Test without API key
    response = client.post("/predict", json=test_input)
    assert response.status_code == 401
    
    # Test with invalid API key
    headers = {"X-API-Key": "invalid_key"}
    response = client.post("/predict", json=test_input, headers=headers)
    assert response.status_code == 401
    
    # Test with valid API key
    headers = {"X-API-Key": "valid_test_key"}
    response = client.post("/predict", json=test_input, headers=headers)
    assert response.status_code == 200 