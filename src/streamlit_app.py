import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🎯",
    layout="wide"
)

# Título e descrição
st.title("🎯 Customer Churn Prediction Dashboard")
st.markdown("""
This dashboard helps predict customer churn probability and provides actionable insights.
""")

# Carregar dados dos clientes
@st.cache_data
def load_customer_data():
    try:
        # Atualizado o caminho do arquivo
        df = pd.read_csv("Bank Customer Churn Prediction.csv")
        # Debug: mostrar as colunas disponíveis
        st.write("Colunas disponíveis:", df.columns.tolist())
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados dos clientes: {str(e)}")
        return None

df_customers = load_customer_data()

# Tabs para diferentes modos
tab1, tab2 = st.tabs(["📋 Cliente Existente", "➕ Novo Cliente"])

with tab1:
    if df_customers is not None:
        st.header("Selecionar Cliente Existente")
        
        # Filtros para encontrar cliente
        # Debug: mostrar valor máximo de customer_id
        max_id = int(df_customers['customer_id'].max()) if 'customer_id' in df_customers.columns else 10000
        st.write(f"ID máximo disponível: {max_id}")
        search_id = st.number_input("Customer ID", min_value=0, max_value=max_id, value=15634602)
        
        # Botão para buscar cliente
        if st.button("Buscar Cliente"):
            # Debug: mostrar a query sendo executada
            st.write(f"Buscando cliente com ID: {search_id}")
            customer = df_customers[df_customers['customer_id'] == search_id]
            
            if not customer.empty:
                st.success("Cliente encontrado!")
                st.write("Dados do Cliente:")
                st.dataframe(customer)
                
                # Preparar dados para predição
                customer_data = customer.iloc[0].to_dict()
                # Remover campos que não são usados na predição
                if 'customer_id' in customer_data:
                    del customer_data['customer_id']
                if 'churn' in customer_data:
                    del customer_data['churn']
                
                # Debug: mostrar dados sendo enviados para API
                st.write("Dados para predição:", customer_data)
                
                # Fazer a predição
                try:
                    response = requests.post("http://localhost:8001/predict", json=customer_data)
                    result = response.json()
                    
                    # Layout em colunas para resultados
                    col1, col2 = st.columns(2)
                    
                    # Coluna 1: Probabilidade de Churn
                    with col1:
                        st.markdown("### Churn Probability")
                        
                        fig = px.pie(values=[result["churn_probability"], 1-result["churn_probability"]], 
                                   names=["Churn Risk", "Retention Probability"],
                                   hole=0.7,
                                   color_discrete_sequence=["#FF6B6B", "#4ECDC4"])
                        
                        fig.update_layout(
                            annotations=[dict(text=f"{result['churn_probability']:.1%}", 
                                            x=0.5, y=0.5, font_size=20, showarrow=False)])
                        st.plotly_chart(fig)
                    
                    # Coluna 2: Insights e Recomendações
                    with col2:
                        st.markdown("### Risk Analysis")
                        
                        risk_level = "High" if result["churn_probability"] > 0.7 else \
                                   "Medium" if result["churn_probability"] > 0.3 else "Low"
                        
                        st.markdown(f"**Risk Level:** {risk_level}")
                        
                        st.markdown("### Recommendations")
                        if risk_level == "High":
                            st.error("⚠️ Immediate action required!")
                            if customer_data['active_member'] == 0:
                                st.markdown("• Engage with customer to increase activity")
                            if customer_data['products_number'] >= 3:
                                st.markdown("• Review product portfolio - possible overload")
                            if customer_data['balance'] == 0:
                                st.markdown("• Investigate account inactivity")
                        elif risk_level == "Medium":
                            st.warning("🔔 Monitor closely")
                            if customer_data['credit_score'] < 650:
                                st.markdown("• Consider credit score improvement programs")
                            if customer_data['tenure'] < 2:
                                st.markdown("• Implement early engagement strategies")
                        else:
                            st.success("✅ Low risk customer")
                            st.markdown("• Consider upselling opportunities")
                            st.markdown("• Maintain regular engagement")
                
                except Exception as e:
                    st.error(f"Error making prediction: {str(e)}")
            else:
                st.warning(f"Cliente com ID {search_id} não encontrado.")

with tab2:
    st.header("Novo Cliente")
    # Formulário de entrada para novo cliente
    with st.form("prediction_form"):
        credit_score = st.slider("Credit Score", 300, 850, 619)
        country = st.selectbox("Country", ["France", "Spain", "Germany"])
        gender = st.selectbox("Gender", ["Female", "Male"])
        age = st.slider("Age", 18, 100, 42)
        tenure = st.slider("Tenure (years)", 0, 10, 2)
        balance = st.number_input("Balance", 0.0, 250000.0, 0.0)
        products_number = st.slider("Number of Products", 1, 4, 1)
        credit_card = st.selectbox("Has Credit Card?", [1, 0])
        active_member = st.selectbox("Is Active Member?", [1, 0])
        estimated_salary = st.number_input("Estimated Salary", 0.0, 200000.0, 101348.88)
        
        submitted = st.form_submit_button("Predict Churn Probability")

    if submitted:
        # Preparar dados para a API
        data = {
            "credit_score": credit_score,
            "country": country,
            "gender": gender,
            "age": age,
            "tenure": tenure,
            "balance": balance,
            "products_number": products_number,
            "credit_card": credit_card,
            "active_member": active_member,
            "estimated_salary": estimated_salary
        }
        
        # Fazer a requisição para a API
        try:
            response = requests.post("http://localhost:8001/predict", json=data)
            result = response.json()
            
            # Layout em colunas
            col1, col2 = st.columns(2)
            
            # Coluna 1: Probabilidade de Churn
            with col1:
                st.markdown("### Churn Probability")
                
                fig = px.pie(values=[result["churn_probability"], 1-result["churn_probability"]], 
                            names=["Churn Risk", "Retention Probability"],
                            hole=0.7,
                            color_discrete_sequence=["#FF6B6B", "#4ECDC4"])
                
                fig.update_layout(
                    annotations=[dict(text=f"{result['churn_probability']:.1%}", 
                                    x=0.5, y=0.5, font_size=20, showarrow=False)])
                st.plotly_chart(fig)
                
            # Coluna 2: Insights e Recomendações
            with col2:
                st.markdown("### Risk Analysis")
                
                risk_level = "High" if result["churn_probability"] > 0.7 else \
                            "Medium" if result["churn_probability"] > 0.3 else "Low"
                
                st.markdown(f"**Risk Level:** {risk_level}")
                
                st.markdown("### Recommendations")
                if risk_level == "High":
                    st.error("⚠️ Immediate action required!")
                    if active_member == 0:
                        st.markdown("• Engage with customer to increase activity")
                    if products_number >= 3:
                        st.markdown("• Review product portfolio - possible overload")
                    if balance == 0:
                        st.markdown("• Investigate account inactivity")
                elif risk_level == "Medium":
                    st.warning("🔔 Monitor closely")
                    if credit_score < 650:
                        st.markdown("• Consider credit score improvement programs")
                    if tenure < 2:
                        st.markdown("• Implement early engagement strategies")
                else:
                    st.success("✅ Low risk customer")
                    st.markdown("• Consider upselling opportunities")
                    st.markdown("• Maintain regular engagement")
                
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")

# Adicionar informações extras
st.markdown("---")
st.markdown("""
### How to use this dashboard:
1. Choose between existing customer or new customer
2. For existing customers:
   - Enter Customer ID
   - Click 'Search Customer'
   - Review customer data and prediction
3. For new customers:
   - Fill in customer information
   - Click 'Predict Churn Probability'
4. Review the prediction and recommendations
5. Take appropriate action based on insights
""") 