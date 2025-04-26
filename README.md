
# 📰 News ETL Pipeline

Este projeto tem como objetivo construir um pipeline ETL (Extract, Transform, Load) para processar notícias relacionadas a acidentes de carro com álcool e armazená-las na AWS S3.

---

## 📂 Estrutura do Projeto

- `scripts/`
  - Scripts para execução **local** do pipeline (sem Airflow).
  - Contém a lógica de **extração**, **transformação** e **upload** para o S3.
  - Pode ser orquestrado diretamente pelo `main_etl.py`.
  
- `docker/`
  - Contém arquivos de configuração para subir ambiente com **Docker Compose**.
  - Sobe containers para:
    - **PostgreSQL** (banco de dados).
    - **Apache Airflow** (orquestração dos pipelines).
  - Subpastas:
    - `dags/`: DAGs utilizadas no Airflow, com scripts de ETL adaptados.
    - `logs/`: Diretório para armazenar logs do Airflow.
    - `plugins/`: Plugins customizados para o Airflow (não utilizados no momento).
  
- `data/`
  - Armazena dados locais extraídos, transformados ou de testes.

- `scripts_s3_functions/`
  - Scripts auxiliares para trabalhar com visualização, extraçaõ e download no S3 (em desenvolvimento).

- `docker-compose.yml`
  - Arquivo principal para subir todos os containers necessários.

- `requirements.txt`
  - Lista de dependências Python necessárias para rodar o projeto localmente.

---

## 🚀 Como Executar

### Ambiente Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/pipelines-news.git
   cd pipelines-news
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure seu arquivo `.env`:
   ```ini
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   AWS_REGION=...
   S3_BUCKET_NAME=...
   NEWS_API_KEY=...
   AIRFLOW__CORE__SQL__ALCHEMY__CONN=...
   AIRFLOW__CORE__LOAD_EXAMPLES=...
   POSTGRES_USER=...
   POSTGRES_PASSWORD=...
   POSTGRES_DB=...
   ```

4. Execute o ETL manualmente:
   ```bash
   python scripts/main_etl.py
   ```

---

### Ambiente com Docker e Airflow

1. Abra o docker, suba os containers:
   ```bash
   cd docker
   docker compose up -d
   ```

2. Acesse o Airflow via navegador:

   [http://localhost:8080](http://localhost:8080)

3. No Airflow:
   - Ative a DAG `etl_pipeline_diario`.
   - Execute o pipeline pela interface.

---

## 📌 Observações

- Garanta que as credenciais AWS estejam corretas para evitar erros no upload para o S3.
- Garanta que as demais API_KEYS estejam corretas.
- Garanta que as credencias do POSTGRES estejam corretas.
- Garante que o docker esteja aberto e as dependencias estejam instaladas.

