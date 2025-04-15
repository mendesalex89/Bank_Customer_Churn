# 🎯 Bank Customer Churn Prediction Project

## 📊 Project Overview
This project implements a machine learning solution to predict customer churn for a bank. Using historical customer data, we've built a system that can identify customers at risk of leaving the bank, allowing for proactive retention measures.

## 🚀 Features
- **Machine Learning Model**: Random Forest classifier trained on historical customer data
- **REST API**: FastAPI-based prediction service
- **Interactive Dashboard**: Streamlit web interface for easy interaction
- **Cloud Deployment**: Fully deployed on Google Cloud using Kubernetes
- **Real-time Predictions**: Instant churn probability calculations
- **Risk Analysis**: Detailed customer risk assessment
- **Automated Recommendations**: Custom retention strategies based on risk level

## 🛠️ Technologies Used
- **Machine Learning**: scikit-learn, pandas, numpy
- **API Development**: FastAPI, pydantic
- **Frontend**: Streamlit
- **Containerization**: Docker
- **Orchestration**: Kubernetes (GKE)
- **Cloud Platform**: Google Cloud
- **Monitoring**: Google Cloud Monitoring (planned)

## 📈 Model Performance
- **Accuracy**: 86.35%
- **Precision**: 79.39%
- **ROC AUC**: 0.8520
- **Cross-validation Score**: 0.8523 ± 0.0066

## 🏗️ Architecture
```
├── 🐳 Docker Container
│   └── 🚀 FastAPI Application
│       └── 🤖 ML Model
├── ☁️ Google Cloud Platform
│   ├── 🎮 Kubernetes Cluster
│   └── 📊 Cloud Monitoring
└── 📱 Streamlit Dashboard
```

## 💻 How to Use

### Local Development
1. Clone the repository
   ```bash
git clone [repository-url]
cd Bank_Customer_Churn
```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API locally
```bash
python src/run_api.py
```

4. Run Streamlit dashboard
```bash
streamlit run src/streamlit_app.py
```

### 🐳 Docker Deployment
1. Build the Docker image
```bash
docker build -t churn-prediction-api .
```

2. Run the container
```bash
docker run -d -p 8001:8001 churn-prediction-api
```

### ☁️ Cloud Deployment
The application is deployed on Google Cloud Platform using:
- Kubernetes Engine (GKE) for container orchestration
- Load Balancer for traffic management
- Secured API endpoints with authentication (planned)
- HTTPS encryption (planned)

Access credentials and endpoints will be provided separately for security reasons.

## 📊 Dashboard Features
1. **Overview Tab**
   - Total customer statistics
   - Churn rate analysis
   - Credit score distribution
   - Balance distribution

2. **Existing Customer Tab**
   - Customer search by ID
   - Advanced filtering options
   - Detailed customer analysis
   - Churn probability prediction

3. **New Customer Tab**
   - Input form for new customers
   - Real-time prediction
   - Risk assessment
   - Customized recommendations

## 🔍 Monitoring (Planned)
- Real-time pod health monitoring
- Resource usage tracking
- API response time monitoring
- Custom alerts and notifications
- Auto-scaling configuration

## 📝 Data Analysis
The model was trained on customer data including:
- Credit Score
- Geography
- Gender
- Age
- Tenure
- Balance
- Number of Products
- Credit Card Status
- Active Member Status
- Estimated Salary

Key findings:
- 20.37% overall churn rate
- Higher churn rate for inactive members
- Correlation between number of products and churn
- Balance level impacts churn probability

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📫 Support
For support, email [your-email] or open an issue in the repository.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Data source: [source]
- Special thanks to all contributors

---
Made with ❤️ for better customer retention