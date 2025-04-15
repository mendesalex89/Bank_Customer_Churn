# Machine Learning Model Documentation

## Model Overview
- **Type**: XGBoost Classifier
- **Version**: 1.0.0
- **Purpose**: Predict customer churn probability for banking customers
- **Performance Metrics**:
  - Accuracy: 0.8635
  - Precision: 0.7939
  - Recall: 0.8520
  - F1-Score: 0.8215

## Features

### Input Features
| Feature | Type | Description | Required |
|---------|------|-------------|-----------|
| CreditScore | Integer | Customer's credit score | Yes |
| Geography | String | Customer's country | Yes |
| Gender | String | Customer's gender | Yes |
| Age | Integer | Customer's age | Yes |
| Tenure | Integer | Years as customer | Yes |
| Balance | Float | Account balance | Yes |
| NumOfProducts | Integer | Number of bank products | Yes |
| HasCrCard | Integer | Has credit card (0/1) | Yes |
| IsActiveMember | Integer | Active member status (0/1) | Yes |
| EstimatedSalary | Float | Estimated annual salary | Yes |

### Feature Engineering
```python
def preprocess_features(data):
    # Categorical encoding
    data['Geography'] = label_encoder.fit_transform(data['Geography'])
    data['Gender'] = label_encoder.fit_transform(data['Gender'])
    
    # Feature scaling
    scaler = StandardScaler()
    numeric_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 'EstimatedSalary']
    data[numeric_features] = scaler.fit_transform(data[numeric_features])
    
    return data
```

## Model Architecture

### XGBoost Parameters
```python
model_params = {
    'max_depth': 6,
    'learning_rate': 0.1,
    'n_estimators': 100,
    'objective': 'binary:logistic',
    'booster': 'gbtree',
    'colsample_bytree': 0.8,
    'subsample': 0.8,
    'random_state': 42
}
```

### Training Process
```python
def train_model(X_train, y_train):
    model = XGBClassifier(**model_params)
    model.fit(
        X_train, 
        y_train,
        eval_set=[(X_val, y_val)],
        early_stopping_rounds=10,
        verbose=True
    )
    return model
```

## Model Performance

### Confusion Matrix
```
[[1527  273]
 [ 201  999]]
```

### Feature Importance
1. Balance (0.285)
2. Age (0.156)
3. EstimatedSalary (0.143)
4. NumOfProducts (0.127)
5. Tenure (0.112)

### Performance by Geography
| Country | Accuracy | Precision | Recall |
|---------|----------|-----------|---------|
| France  | 0.872    | 0.801     | 0.863   |
| Germany | 0.858    | 0.785     | 0.842   |
| Spain   | 0.861    | 0.795     | 0.851   |

## Model Deployment

### Saving the Model
```python
# Save model
model.save_model('models/xgboost_churn_v1.json')

# Save preprocessing objects
joblib.dump(label_encoder, 'models/label_encoder.joblib')
joblib.dump(scaler, 'models/scaler.joblib')
```

### Loading in Production
```python
def load_model():
    model = XGBClassifier()
    model.load_model('models/xgboost_churn_v1.json')
    label_encoder = joblib.load('models/label_encoder.joblib')
    scaler = joblib.load('models/scaler.joblib')
    return model, label_encoder, scaler
```

## Monitoring and Maintenance

### Model Monitoring
- Input feature distributions
- Prediction distributions
- Model performance metrics
- Response times

### Retraining Criteria
1. Performance drop below 80% accuracy
2. Feature drift > 20%
3. Every 3 months with new data

### Version Control
- Models stored in GCS bucket
- Version tracking in MLflow
- A/B testing for new versions

## Risk Levels

### Classification Rules
```python
def get_risk_level(probability):
    if probability >= 0.7:
        return "High"
    elif probability >= 0.3:
        return "Medium"
    else:
        return "Low"
```

### Recommended Actions
- **High Risk**:
  - Immediate customer contact
  - Personalized retention offers
  - Account review
- **Medium Risk**:
  - Scheduled check-in
  - Product recommendations
  - Satisfaction survey
- **Low Risk**:
  - Regular monitoring
  - Standard promotions
  - Periodic review

## Model Limitations

### Known Limitations
1. Limited to retail banking customers
2. May not perform well for new markets
3. Requires all features to be present

### Edge Cases
1. New customers (< 1 month tenure)
2. Very high net worth individuals
3. Corporate accounts

## Future Improvements

### Planned Enhancements
1. Add more features:
   - Transaction patterns
   - Customer service interactions
   - Product usage metrics

2. Model improvements:
   - Deep learning implementation
   - Automated feature selection
   - Real-time model updates

3. Infrastructure:
   - Model versioning
   - A/B testing framework
   - Automated retraining pipeline 