import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para fazer predição
def make_prediction(customer_data):
    try:
        logger.info(f"Attempting to make prediction with data: {customer_data}")
        # Atualizado para usar o endpoint em produção
        response = requests.post("http://34.69.103.18/predict", json=customer_data)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Prediction successful: {result}")
            return result
        else:
            logger.error(f"API Error: Status {response.status_code}, Response: {response.text}")
            st.error(f"Error making prediction. Status code: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        logger.error("Connection error with production API")
        st.error("Connection error with API. Please check your internet connection.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        st.error(f"Unexpected error making prediction: {str(e)}")
        return None

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
        df = pd.read_csv("Bank Customer Churn Prediction.csv")
        return df
    except Exception as e:
        st.error(f"Error loading customer data: {str(e)}")
        return None

df_customers = load_customer_data()

# Tabs para diferentes modos
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📋 Existing Customer", "➕ New Customer"])

with tab1:
    if df_customers is not None:
        st.header("Customer Overview")
        
        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Customers", len(df_customers))
        with col2:
            churn_rate = (df_customers['churn'] == 1).mean() * 100
            st.metric("Churn Rate", f"{churn_rate:.1f}%")
        with col3:
            avg_balance = df_customers['balance'].mean()
            st.metric("Average Balance", f"${avg_balance:,.2f}")
        with col4:
            avg_credit_score = df_customers['credit_score'].mean()
            st.metric("Average Credit Score", f"{avg_credit_score:.0f}")
        
        # Filtros
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        with col1:
            country_filter = st.multiselect("Country", df_customers['country'].unique())
        with col2:
            credit_score_range = st.slider("Credit Score", 
                                         int(df_customers['credit_score'].min()),
                                         int(df_customers['credit_score'].max()),
                                         (300, 850))
        with col3:
            balance_range = st.slider("Balance", 
                                    float(df_customers['balance'].min()),
                                    float(df_customers['balance'].max()),
                                    (0.0, 250000.0))
        
        # Aplicar filtros
        filtered_df = df_customers.copy()
        if country_filter:
            filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]
        filtered_df = filtered_df[
            (filtered_df['credit_score'].between(credit_score_range[0], credit_score_range[1])) &
            (filtered_df['balance'].between(balance_range[0], balance_range[1]))
        ]
        
        # Visualizações
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Churn Distribution by Country")
            fig = px.bar(filtered_df.groupby('country')['churn'].mean().reset_index(),
                        x='country', y='churn',
                        title="Churn Rate by Country",
                        labels={'churn': 'Churn Rate', 'country': 'Country'})
            st.plotly_chart(fig)
            
        with col2:
            st.subheader("Credit Score vs Churn")
            fig = px.box(filtered_df, x='churn', y='credit_score',
                        title="Credit Score by Churn Status",
                        labels={'churn': 'Churn', 'credit_score': 'Credit Score'})
            st.plotly_chart(fig)
        
        # Tabela de dados filtrados
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

with tab2:
    if df_customers is not None:
        st.header("Select Existing Customer")
        
        # Opções de busca
        search_method = st.radio("Search Method", ["Customer ID", "Advanced Filters"])
        
        if search_method == "Customer ID":
            # Criar uma lista de todos os IDs disponíveis
            available_ids = df_customers['customer_id'].unique().tolist()
            max_id = int(df_customers['customer_id'].max())
            min_id = int(df_customers['customer_id'].min())
            
            # Mostrar informação sobre a quantidade total de clientes
            total_customers = len(available_ids)
            st.info(f"Total customers in database: {total_customers}")
            
            # Opção para ver todos os IDs
            if st.checkbox("View all available IDs"):
                st.write("Complete list of IDs:")
                cols = st.columns(4)
                for idx, customer_id in enumerate(sorted(available_ids)):
                    cols[idx % 4].write(f"• {customer_id}")
            
            # Input do ID com validação
            search_id = st.number_input(
                "Customer ID",
                min_value=min_id,
                max_value=max_id,
                value=min_id,
                help=f"Enter any ID between {min_id} and {max_id}"
            )
            
            if search_id not in available_ids:
                st.warning(f"ID {search_id} does not exist in the database. Please use one of the available IDs.")
            
            search_button = st.button("Search Customer")
            
            if search_button:
                if search_id in available_ids:
                    customer = df_customers[df_customers['customer_id'] == search_id]
                    st.success(f"Customer found!")
                else:
                    st.error("Customer not found. Please use one of the available IDs.")
                    customer = pd.DataFrame()
        else:
            # Advanced filters
            col1, col2, col3 = st.columns(3)
            with col1:
                country = st.selectbox("Country", df_customers['country'].unique())
            with col2:
                credit_score = st.slider("Credit Score", 300, 850, 619)
            with col3:
                balance = st.number_input("Minimum Balance", 0.0, 250000.0, 0.0)
            
            search_button = st.button("Search Customers")
            
            if search_button:
                customer = df_customers[
                    (df_customers['country'] == country) &
                    (df_customers['credit_score'] >= credit_score) &
                    (df_customers['balance'] >= balance)
                ]
        
        if 'search_button' in locals() and search_button:
            if not customer.empty:
                st.success(f"Found {len(customer)} customer(s)!")
                st.write("Customer(s) Data:")
                st.dataframe(customer)
                
                # Se for apenas um cliente, mostrar análise detalhada
                if len(customer) == 1:
                    customer_data = customer.iloc[0].to_dict()
                    if 'customer_id' in customer_data:
                        del customer_data['customer_id']
                    if 'churn' in customer_data:
                        del customer_data['churn']
                    
                    result = make_prediction(customer_data)
                    if result:
                        col1, col2 = st.columns(2)
                        
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
            else:
                st.warning("No customer found with the specified criteria.")

with tab3:
    st.header("New Customer")
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
1. Choose between existing customer or new customer analysis
2. For existing customers:
   - Enter Customer ID or use Advanced Filters
   - Click 'Search Customer'
   - Review customer data and prediction
3. For new customers:
   - Fill in all customer information
   - Click 'Predict Churn Probability'
4. Review the prediction results and recommendations
5. Take appropriate action based on risk level

### Risk Levels:
- High Risk (>70%): Immediate action required
- Medium Risk (30-70%): Monitor closely
- Low Risk (<30%): Regular engagement
""") 