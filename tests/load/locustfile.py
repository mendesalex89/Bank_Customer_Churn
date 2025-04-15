from locust import HttpUser, task, between
import json
import random

class ChurnPredictionUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Setup data needed for tests"""
        self.headers = {"X-API-Key": "valid_test_key"}
        self.sample_customers = self._generate_sample_customers()
    
    def _generate_sample_customers(self):
        """Generate a list of sample customers for testing"""
        countries = ["France", "Germany", "Spain"]
        genders = ["Male", "Female"]
        
        customers = []
        for _ in range(10):
            customer = {
                "CreditScore": random.randint(300, 850),
                "Geography": random.choice(countries),
                "Gender": random.choice(genders),
                "Age": random.randint(18, 95),
                "Tenure": random.randint(0, 10),
                "Balance": random.uniform(0, 250000),
                "NumOfProducts": random.randint(1, 4),
                "HasCrCard": random.randint(0, 1),
                "IsActiveMember": random.randint(0, 1),
                "EstimatedSalary": random.uniform(30000, 200000)
            }
            customers.append(customer)
        return customers
    
    @task(3)
    def predict_single(self):
        """Test single prediction endpoint"""
        customer = random.choice(self.sample_customers)
        self.client.post(
            "/predict",
            json=customer,
            headers=self.headers
        )
    
    @task(1)
    def predict_batch(self):
        """Test batch prediction endpoint"""
        batch_size = random.randint(2, 5)
        customers = random.sample(self.sample_customers, batch_size)
        self.client.post(
            "/predict/batch",
            json={"customers": customers},
            headers=self.headers
        )
    
    @task(5)
    def get_health(self):
        """Test health check endpoint"""
        self.client.get("/health")
    
    @task(1)
    def get_model_info(self):
        """Test model info endpoint"""
        self.client.get("/model/info", headers=self.headers) 