from fastapi import FastAPI, HTTPException
from .schemas.customer import CustomerBase, CustomerResponse
from .services.prediction import ChurnPredictor
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Bank Customer Churn Prediction API",
    description="API para prever a probabilidade de churn de clientes bancários",
    version="1.0.0"
)

# Inicializa o predictor
predictor = ChurnPredictor()

@app.post("/predict", response_model=CustomerResponse)
async def predict_churn(customer: CustomerBase):
    try:
        # Converte o modelo Pydantic para dicionário
        customer_data = customer.dict()
        logger.info(f"Recebida requisição para cliente: {customer_data}")
        
        # Faz a predição
        churn_probability, is_likely_to_churn = predictor.predict(customer_data)
        
        # Retorna a resposta
        return CustomerResponse(
            churn_probability=float(churn_probability),
            is_likely_to_churn=bool(is_likely_to_churn)
        )
    except Exception as e:
        logger.error(f"Erro ao processar requisição: {str(e)}")
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

@app.get("/")
async def root():
    return {
        "message": "Bank Customer Churn Prediction API",
        "docs": "/docs",
        "health": "OK"
    } 