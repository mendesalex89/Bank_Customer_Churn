import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChurnPredictor:
    def __init__(self):
        # Ajustando o caminho para considerar a raiz do projeto
        base_path = Path(__file__).parent.parent.parent.parent
        model_path = base_path / "models" / "random_forest_model.joblib"
        feature_names_path = base_path / "models" / "feature_names.joblib"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        if not feature_names_path.exists():
            raise FileNotFoundError(f"Feature names file not found at {feature_names_path}")
            
        self.model = joblib.load(model_path)
        self.feature_names = joblib.load(feature_names_path)
        logger.info(f"Modelo carregado com {len(self.feature_names)} features")

    def prepare_features(self, customer_data: dict) -> pd.DataFrame:
        """
        Prepara os dados do cliente para predição, aplicando o mesmo
        pré-processamento usado no treinamento.
        """
        # Criar DataFrame com uma linha
        df = pd.DataFrame([customer_data])
        logger.info(f"Dados recebidos: {customer_data}")
        
        # Aplicar one-hot encoding
        df_encoded = pd.get_dummies(df, columns=['country', 'gender'])
        logger.info(f"Colunas após encoding: {df_encoded.columns.tolist()}")
        
        # Garantir que todas as colunas necessárias estão presentes
        for feature in self.feature_names:
            if feature not in df_encoded.columns:
                df_encoded[feature] = 0
                logger.info(f"Adicionada coluna ausente: {feature}")
                
        # Reordenar as colunas para match com o treinamento
        df_final = df_encoded[self.feature_names]
        logger.info(f"Shape final dos dados: {df_final.shape}")
        return df_final

    def predict(self, customer_data: dict) -> tuple[float, bool]:
        """
        Predict the probability of churn for a customer.
        
        Args:
            customer_data (dict): Customer information
            
        Returns:
            tuple[float, bool]: (churn probability, is likely to churn)
        """
        # Preparar os dados
        df = self.prepare_features(customer_data)
        
        # Get probability predictions
        proba = self.model.predict_proba(df)[0]
        churn_probability = proba[1]  # Probability of class 1 (churn)
        logger.info(f"Probabilidade calculada: {churn_probability}")
        
        # Define threshold for churn prediction (can be adjusted based on business needs)
        threshold = 0.5
        is_likely_to_churn = churn_probability >= threshold
        
        return churn_probability, is_likely_to_churn 