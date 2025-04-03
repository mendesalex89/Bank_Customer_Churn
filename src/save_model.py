import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

def load_and_prepare_data():
    # Carrega os dados
    df = pd.read_csv("Bank Customer Churn Prediction.csv")
    
    # Remove a coluna customer_id se existir
    if 'customer_id' in df.columns:
        df = df.drop('customer_id', axis=1)
    
    # Separar features e target
    X = df.drop('churn', axis=1)
    y = df['churn']
    
    # Encoding das variáveis categóricas
    X = pd.get_dummies(X, columns=['country', 'gender'], drop_first=True)
    
    return X, y

def train_model(X, y):
    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Criar e treinar o modelo
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42
    )
    
    rf_model.fit(X_train, y_train)
    return rf_model

def save_model(model, feature_names):
    # Criar diretório models se não existir
    Path("models").mkdir(exist_ok=True)
    
    # Salvar o modelo
    model_path = "models/random_forest_model.joblib"
    joblib.dump(model, model_path)
    
    # Salvar os nomes das features
    feature_names_path = "models/feature_names.joblib"
    joblib.dump(feature_names, feature_names_path)
    
    print(f"Modelo salvo em: {model_path}")
    print(f"Nomes das features salvos em: {feature_names_path}")

if __name__ == "__main__":
    print("Carregando e preparando os dados...")
    X, y = load_and_prepare_data()
    
    print("Treinando o modelo Random Forest...")
    model = train_model(X, y)
    
    print("Salvando o modelo e os nomes das features...")
    save_model(model, list(X.columns))
    
    print("Processo concluído com sucesso!") 