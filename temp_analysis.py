import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('Bank Customer Churn Prediction.csv')

# Basic statistics
print("=== Estatísticas Básicas ===")
print("\nShape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())

# Target distribution
churn_dist = df['churn'].value_counts(normalize=True) * 100
print("\n=== Distribuição do Churn ===")
print(churn_dist)

# Numeric columns statistics
numeric_cols = ['credit_score', 'age', 'tenure', 'balance', 'products_number', 'estimated_salary']
print("\n=== Estatísticas das Variáveis Numéricas ===")
print(df[numeric_cols].describe())

# Categorical columns distribution
categorical_cols = ['country', 'gender']
print("\n=== Distribuição das Variáveis Categóricas ===")
for col in categorical_cols:
    print(f"\n{col}:\n", df[col].value_counts(normalize=True) * 100) 