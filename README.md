# Bank Customer Churn Prediction

Este projeto tem como objetivo desenvolver um modelo de machine learning para prever a probabilidade de churn (cancelamento) de clientes bancários. O modelo será disponibilizado através de uma API REST construída com FastAPI e deployada no Google Cloud.

## Estrutura do Projeto

```
├── notebooks/          # Jupyter notebooks para análise exploratória
├── src/               # Código fonte do projeto
│   ├── api/          # Código da API FastAPI
│   ├── data/         # Scripts de processamento de dados
│   ├── features/     # Scripts de engenharia de features
│   ├── models/       # Scripts de treinamento e avaliação de modelos
│   ├── utils/        # Funções utilitárias
│   ├── visualization/# Scripts de visualização
│   └── tests/        # Testes unitários
├── requirements.txt   # Dependências do projeto
└── README.md         # Este arquivo
```

## Configuração do Ambiente

1. Clone o repositório
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Dataset

O dataset contém informações sobre clientes bancários, incluindo:
- Dados demográficos (idade, país, gênero)
- Informações bancárias (score de crédito, saldo, produtos)
- Histórico de relacionamento (tempo como cliente, membro ativo)
- Variável alvo: churn (0: manteve-se cliente, 1: cancelou)

## Desenvolvimento

O projeto está sendo desenvolvido em fases:
1. Análise exploratória e preparação dos dados
2. Engenharia de features
3. Treinamento e otimização de modelos
4. Desenvolvimento da API
5. Deploy no Google Cloud

## Métricas de Avaliação

O modelo será avaliado usando:
- AUC-ROC
- Precisão
- Recall
- F1-Score

## API

A API será desenvolvida usando FastAPI e incluirá:
- Endpoint de predição
- Documentação automática (Swagger)
- Validação de dados de entrada
- Logs e monitoramento

## Deploy

O deploy será realizado no Google Cloud Platform utilizando:
- Containerização com Docker
- Google Cloud Run para hospedagem
- Monitoramento e logging

## Autor

[Seu Nome]

## Licença

Este projeto está sob a licença MIT.