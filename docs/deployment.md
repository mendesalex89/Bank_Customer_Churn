# Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Monitoring Setup](#monitoring-setup)

## Prerequisites

### Required Tools
- Python 3.9+
- Docker
- kubectl
- Google Cloud SDK
- Git

### Environment Setup
```bash
# Install Google Cloud SDK
# For Ubuntu/Debian
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-sdk

# Initialize Google Cloud
gcloud init

# Install kubectl
gcloud components install kubectl
```

## Local Deployment

1. **Clone the Repository**
```bash
git clone [repository-url]
cd Bank_Customer_Churn
```

2. **Set Up Python Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the API**
```bash
uvicorn src.api.main:app --reload --port 8000
```

4. **Run Streamlit Dashboard**
```bash
streamlit run src/streamlit_app.py
```

## Docker Deployment

1. **Build the Docker Image**
```bash
docker build -t churn-prediction-api:latest .
```

2. **Run the Container**
```bash
docker run -d -p 8001:8001 --name churn-api churn-prediction-api:latest
```

3. **Check Container Logs**
```bash
docker logs -f churn-api
```

## Kubernetes Deployment

1. **Create GKE Cluster**
```bash
gcloud container clusters create churn-prediction-cluster \
    --num-nodes=2 \
    --machine-type=e2-medium \
    --zone=us-central1-a
```

2. **Get Credentials**
```bash
gcloud container clusters get-credentials churn-prediction-cluster --zone=us-central1-a
```

3. **Deploy Application**
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

4. **Verify Deployment**
```bash
kubectl get pods
kubectl get services
```

## Monitoring Setup

1. **Enable Google Cloud Monitoring**
```bash
gcloud services enable monitoring.googleapis.com
```

2. **Configure Alerts**
- CPU Usage > 80%
- Memory Usage > 80%
- API Response Time > 1s

3. **Access Monitoring**
- Go to Google Cloud Console
- Navigate to Monitoring > Overview
- Check the "Churn Prediction" dashboard

## Troubleshooting

### Common Issues

1. **Pod Pending Status**
```bash
kubectl describe pod [pod-name]
# Check for resource constraints or configuration issues
```

2. **API Not Responding**
```bash
kubectl logs [pod-name]
# Check for application errors
```

3. **High Resource Usage**
```bash
kubectl top pods
# Monitor resource consumption
```

## Maintenance

### Regular Tasks
1. Update dependencies monthly
2. Check for security vulnerabilities
3. Monitor resource usage
4. Backup configuration files

### Scaling
```bash
kubectl scale deployment churn-prediction-api --replicas=3
```

## Security Best Practices
1. Use secrets for sensitive data
2. Enable HTTPS
3. Implement authentication
4. Regular security updates 