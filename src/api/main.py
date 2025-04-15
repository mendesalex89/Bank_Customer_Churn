from fastapi import FastAPI, HTTPException, Request
from .schemas.customer import CustomerBase, CustomerResponse
from .services.prediction import ChurnPredictor
import logging
import time
from ..monitoring import setup_monitoring

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar o monitoramento
metrics = setup_monitoring("churn-prediction-api")

app = FastAPI(
    title="Bank Customer Churn Prediction API",
    description="API para prever a probabilidade de churn de clientes bancários",
    version="1.0.0"
)

# Inicializa o predictor
predictor = ChurnPredictor()

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    """Middleware para coletar métricas de todas as requisições."""
    start_time = time.time()
    
    try:
        # Incrementa o contador de requisições
        metrics["request_counter"].add(1)
        
        # Processa a requisição
        response = await call_next(request)
        
        # Registra a latência
        latency = (time.time() - start_time) * 1000  # Converte para milissegundos
        metrics["latency_histogram"].record(latency)
        
        return response
        
    except Exception as e:
        # Incrementa o contador de erros
        metrics["error_counter"].add(1)
        raise e

@app.post("/predict", response_model=CustomerResponse)
async def predict_churn(customer: CustomerBase):
    try:
        start_time = time.time()
        
        # Converte o modelo Pydantic para dicionário
        customer_data = customer.dict()
        logger.info(f"Recebida requisição para cliente: {customer_data}")
        
        # Faz a predição
        churn_probability, is_likely_to_churn = predictor.predict(customer_data)
        
        # Registra a probabilidade de churn no histograma
        metrics["prediction_histogram"].record(float(churn_probability))
        
        # Registra a latência da predição
        latency = (time.time() - start_time) * 1000  # Converte para milissegundos
        metrics["latency_histogram"].record(latency)
        
        # Retorna a resposta
        return CustomerResponse(
            churn_probability=float(churn_probability),
            is_likely_to_churn=bool(is_likely_to_churn)
        )
    except Exception as e:
        logger.error(f"Erro ao processar requisição: {str(e)}")
        metrics["error_counter"].add(1)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-profiles")
async def test_different_profiles():
    """Testa diferentes perfis de clientes para verificar variações nas predições"""
    test_profiles = [
        {
            "description": "Cliente jovem com alto saldo",
            "data": {
                "credit_score": 750,
                "country": "France",
                "gender": "Male",
                "age": 25,
                "tenure": 1,
                "balance": 150000.0,
                "products_number": 1,
                "credit_card": 1,
                "active_member": 1,
                "estimated_salary": 80000.0
            }
        },
        {
            "description": "Cliente sênior com baixo engajamento",
            "data": {
                "credit_score": 600,
                "country": "Germany",
                "gender": "Female",
                "age": 65,
                "tenure": 10,
                "balance": 5000.0,
                "products_number": 3,
                "credit_card": 0,
                "active_member": 0,
                "estimated_salary": 45000.0
            }
        },
        {
            "description": "Cliente de meia idade estável",
            "data": {
                "credit_score": 680,
                "country": "Spain",
                "gender": "Male",
                "age": 45,
                "tenure": 8,
                "balance": 75000.0,
                "products_number": 2,
                "credit_card": 1,
                "active_member": 1,
                "estimated_salary": 95000.0
            }
        }
    ]
    
    results = []
    for profile in test_profiles:
        prob, is_churn = predictor.predict(profile["data"])
        results.append({
            "description": profile["description"],
            "prediction": {
                "churn_probability": float(prob),
                "is_likely_to_churn": bool(is_churn)
            }
        })
    
    return results

@app.get("/metrics")
async def get_metrics():
    """Retorna métricas básicas da API"""
    return {
        "status": "healthy",
        "total_requests": metrics["request_counter"].get_value(),
        "total_errors": metrics["error_counter"].get_value(),
        "average_latency": metrics["latency_histogram"].get_average()
    }

@app.get("/")
async def root():
    return {
        "message": "Bank Customer Churn Prediction API",
        "docs": "/docs",
        "health": "OK",
        "metrics": "/metrics"
    } 