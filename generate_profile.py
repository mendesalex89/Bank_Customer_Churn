import os
import pandas as pd
from pandas_profiling import ProfileReport

# Criar diretório para relatórios se não existir
os.makedirs('reports', exist_ok=True)

print("Carregando o dataset...")
df = pd.read_csv('Bank Customer Churn Prediction.csv')
print(f"Dataset carregado com formato: {df.shape}")

print("Gerando relatório Pandas Profiling...")
profile = ProfileReport(df, 
                       title="Bank Customer Churn Dataset Profiling Report",
                       minimal=False,
                       explorative=True)

print("Salvando relatório HTML...")
profile.to_file("reports/churn_profile_report.html")

print("\nRelatório salvo em: reports/churn_profile_report.html")
print("Abra este arquivo em um navegador para visualizar o relatório completo.") 