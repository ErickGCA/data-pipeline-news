FROM apache/airflow:2.6.1

USER root

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copiar requirements
COPY requirements.txt /requirements.txt

# Instalar dependências Python
RUN pip install --no-cache-dir -r /requirements.txt

# Criar diretórios para dados do pipeline
RUN mkdir -p /opt/airflow/data/raw /opt/airflow/data/processed /opt/airflow/logs && \
    chown -R airflow:root /opt/airflow/data /opt/airflow/logs