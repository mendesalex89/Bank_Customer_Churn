import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Churn Prediction Monitoring", layout="wide")

st.title("🔍 Dashboard de Monitoramento - Churn Prediction")

# Configuração das colunas
col1, col2 = st.columns(2)

# Função para obter métricas da API
def get_api_metrics():
    try:
        response = requests.get("http://localhost:8000/metrics")
        return response.json()
    except:
        return None

# Função para obter métricas do Kubernetes
def get_kubernetes_metrics():
    try:
        response = requests.get("http://34.69.103.18/metrics")
        return response.json()
    except:
        return None

# Atualização automática
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# Métricas em tempo real
with col1:
    st.subheader("📊 Métricas em Tempo Real")
    
    metrics = get_api_metrics()
    if metrics:
        col1_1, col1_2, col1_3 = st.columns(3)
        
        with col1_1:
            st.metric("Total de Requisições", metrics.get("total_requests", 0))
        
        with col1_2:
            st.metric("Erros", metrics.get("total_errors", 0))
        
        with col1_3:
            latency = metrics.get("average_latency", 0)
            st.metric("Latência Média", f"{latency:.2f}ms")
    else:
        st.warning("Não foi possível obter métricas da API")

# Métricas do Kubernetes
with col2:
    st.subheader("🚀 Status do Cluster")
    
    k8s_metrics = get_kubernetes_metrics()
    if k8s_metrics:
        col2_1, col2_2, col2_3 = st.columns(3)
        
        with col2_1:
            st.metric("Pods Ativos", k8s_metrics.get("active_pods", 0))
        
        with col2_2:
            cpu = k8s_metrics.get("cpu_usage", 0)
            st.metric("CPU Usage", f"{cpu:.1f}%")
        
        with col2_3:
            memory = k8s_metrics.get("memory_usage", 0)
            st.metric("Memory Usage", f"{memory:.1f}%")
    else:
        st.warning("Não foi possível obter métricas do Kubernetes")

# Gráficos
st.subheader("📈 Análise de Predições")

# Simulação de dados para os gráficos
if 'predictions_data' not in st.session_state:
    st.session_state.predictions_data = []

# Adicionar dados simulados
current_time = datetime.now()
if (current_time - st.session_state.last_refresh).seconds >= 5:
    metrics = get_api_metrics()
    if metrics:
        st.session_state.predictions_data.append({
            'timestamp': current_time,
            'requests': metrics.get('total_requests', 0),
            'errors': metrics.get('total_errors', 0),
            'latency': metrics.get('average_latency', 0)
        })
        st.session_state.last_refresh = current_time

# Criar DataFrame
if st.session_state.predictions_data:
    df = pd.DataFrame(st.session_state.predictions_data)
    
    # Gráficos
    col3, col4 = st.columns(2)
    
    with col3:
        fig_requests = px.line(df, x='timestamp', y='requests', 
                             title='Requisições ao Longo do Tempo')
        st.plotly_chart(fig_requests, use_container_width=True)
    
    with col4:
        fig_latency = px.line(df, x='timestamp', y='latency',
                             title='Latência ao Longo do Tempo (ms)')
        st.plotly_chart(fig_latency, use_container_width=True)

# Atualização automática
time.sleep(5)
st.experimental_rerun() 