# Troubleshooting Guide

## Common Issues and Solutions

### API Issues

#### 1. API Not Responding
**Symptoms:**
- Timeout errors
- 502 Bad Gateway
- Connection refused

**Solutions:**
1. Check pod status:
```bash
kubectl get pods
kubectl describe pod [pod-name]
```

2. Check logs:
```bash
kubectl logs [pod-name]
```

3. Verify resources:
```bash
kubectl top pods
```

#### 2. High Latency
**Symptoms:**
- Slow response times
- Timeout errors

**Solutions:**
1. Check CPU/Memory usage:
```bash
kubectl top pods
```

2. Review recent requests:
```bash
kubectl logs [pod-name] | grep "Response time"
```

3. Scale resources if needed:
```bash
kubectl scale deployment churn-prediction-api --replicas=3
```

### Model Issues

#### 1. Incorrect Predictions
**Symptoms:**
- Unexpected churn probabilities
- Inconsistent risk levels

**Solutions:**
1. Verify input data format
2. Check model version:
```bash
curl http://34.69.103.18/model/info
```

3. Review model logs:
```bash
kubectl logs [pod-name] | grep "prediction"
```

#### 2. Model Loading Errors
**Symptoms:**
- 500 Internal Server Error
- Model not found errors

**Solutions:**
1. Check model path in configuration
2. Verify model file exists in container
3. Review initialization logs

### Infrastructure Issues

#### 1. Kubernetes Cluster
**Symptoms:**
- Pods in pending state
- Resource constraints

**Solutions:**
1. Check node status:
```bash
kubectl get nodes
kubectl describe node [node-name]
```

2. Review resource quotas:
```bash
kubectl describe resourcequota
```

3. Check events:
```bash
kubectl get events --sort-by='.lastTimestamp'
```

#### 2. Network Issues
**Symptoms:**
- Service unavailable
- DNS resolution failures

**Solutions:**
1. Check service status:
```bash
kubectl get services
```

2. Verify endpoints:
```bash
kubectl get endpoints
```

3. Test network policies:
```bash
kubectl get networkpolicies
```

## Monitoring and Debugging

### 1. Logging
Access application logs:
```bash
# Last 100 lines
kubectl logs [pod-name] --tail=100

# Stream logs
kubectl logs -f [pod-name]

# Logs with timestamps
kubectl logs [pod-name] --timestamps=true
```

### 2. Metrics
View performance metrics:
```bash
# Pod metrics
kubectl top pods

# Node metrics
kubectl top nodes
```

### 3. Debugging
Debug running pods:
```bash
# Interactive shell
kubectl exec -it [pod-name] -- /bin/bash

# Copy files
kubectl cp [pod-name]:/path/to/file ./local-file
```

## Recovery Procedures

### 1. Pod Recovery
```bash
# Delete problematic pod
kubectl delete pod [pod-name]

# Restart deployment
kubectl rollout restart deployment churn-prediction-api
```

### 2. Backup and Restore
```bash
# Backup configuration
kubectl get all -o yaml > backup.yaml

# Restore from backup
kubectl apply -f backup.yaml
```

## Contact Support
For issues not resolved by this guide:
1. Open GitHub issue
2. Contact cloud support
3. Email development team 