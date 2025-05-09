# News ETL Pipeline 📰

Bem-vindo à documentação do pipeline ETL para extração e análise de notícias sobre acidentes com álcool.

## Visão Geral

Este projeto implementa um pipeline completo de extração, transformação e carregamento (ETL) de notícias relacionadas a acidentes de trânsito envolvendo álcool. O pipeline segue princípios SOLID de design, tornando-o modular, manutenível e extensível.

## Características Principais

- 🔍 **Extração** - Coleta de dados de múltiplas fontes de notícias (NewsAPI, GNews)
- ⚙️ **Transformação** - Processamento, limpeza e classificação das notícias
- 💾 **Carregamento** - Armazenamento em PostgreSQL e Amazon S3
- 🔄 **Orquestração** - Automação do fluxo de trabalho com Apache Airflow
- 🧱 **Arquitetura SOLID** - Design orientado a interfaces para alta coesão e baixo acoplamento

## Tecnologias Utilizadas

- Python 3.7+
- Apache Airflow
- PostgreSQL
- Amazon S3
- Docker e Docker Compose

## Começando

Para executar este projeto localmente:

```bash
# Clonar o repositório
git clone https://github.com/ErickGCA/data-pipeline-news.git

# Navegar até o diretório do projeto
cd data-pipeline-news

# Iniciar os serviços Docker (Airflow, PostgreSQL)
cd docker
docker-compose up -d
```

Acesse a interface web do Airflow em http://localhost:8080 para monitorar e executar o pipeline. 