# API Documentation

## Overview
The Churn Prediction API provides endpoints for predicting customer churn probability and risk levels. Built with FastAPI, it offers real-time predictions using our trained XGBoost model.

## Base URL
- Local: `http://localhost:8001`
- Production: `http://34.69.103.18`

## Authentication
Currently using basic API key authentication. Include the API key in the header:
```
X-API-Key: your-api-key
```

## Endpoints

### 1. Health Check
```http
GET /health
```
Returns the API's operational status.

#### Response
```json
{
    "status": "healthy",
    "version": "1.0.0"
}
```

### 2. Predict Churn
```http
POST /predict
```
Predicts the probability of customer churn based on provided features.

#### Request Body
```json
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
}
```

#### Response
```json
{
    "customer_id": "20240414_182413",
    "churn_probability": 0.08,
    "is_likely_to_churn": false,
    "risk_level": "Low",
    "recommendations": [
        "Offer premium services",
        "Schedule regular check-ins"
    ]
}
```

### 3. Batch Predictions
```http
POST /predict/batch
```
Processes multiple customer records for batch predictions.

#### Request Body
```json
{
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
        }
    ]
}
```

#### Response
```json
{
    "predictions": [
        {
            "customer_index": 0,
            "churn_probability": 0.08,
            "is_likely_to_churn": false,
            "risk_level": "Low"
        }
    ],
    "batch_id": "batch_20240414_182413"
}
```

### 4. Model Information
```http
GET /model/info
```
Returns information about the current model version and performance metrics.

#### Response
```json
{
    "model_version": "1.0.0",
    "last_trained": "2024-04-14",
    "performance_metrics": {
        "accuracy": 0.8635,
        "precision": 0.7939,
        "recall": 0.8520,
        "f1_score": 0.8215
    }
}
```

## Error Handling

### Error Responses
```json
{
    "error": true,
    "message": "Error description",
    "code": "ERROR_CODE",
    "timestamp": "2024-04-14T18:24:13Z"
}
```

### Common Error Codes
- `400`: Bad Request - Invalid input data
- `401`: Unauthorized - Invalid or missing API key
- `422`: Validation Error - Input validation failed
- `500`: Internal Server Error - Server-side error

## Rate Limiting
- 100 requests per minute per API key
- Batch predictions count as multiple requests based on batch size

## Best Practices
1. Use batch predictions for multiple records
2. Include error handling in your client code
3. Monitor response times and errors
4. Cache results when appropriate

## SDK Examples

### Python
```python
import requests

def predict_churn(customer_data, api_key):
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'http://34.69.103.18/predict',
        json=customer_data,
        headers=headers
    )
    
    return response.json()
```

### curl
```bash
curl -X POST http://34.69.103.18/predict \
    -H "X-API-Key: your-api-key" \
    -H "Content-Type: application/json" \
    -d '{"CreditScore": 619, "Geography": "France"...}'
``` 