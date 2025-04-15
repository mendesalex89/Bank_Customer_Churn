#!/bin/bash

# Inicia a API em background
python src/run_api.py &

# Aguarda alguns segundos para a API iniciar
sleep 5

# Inicia o Streamlit
streamlit run src/streamlit_app.py 