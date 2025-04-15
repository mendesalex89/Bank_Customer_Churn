# Use a imagem base do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
COPY src/ src/
COPY models/ models/
COPY data/ data/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe as portas necessárias
EXPOSE 8000
EXPOSE 8501

# Cria um script para iniciar ambos os serviços
COPY start.sh .
RUN chmod +x start.sh

# Define o comando para iniciar os serviços
CMD ["./start.sh"] 