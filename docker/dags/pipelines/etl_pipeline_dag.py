from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
from dotenv import load_dotenv
from utils.setup_all_directories import setup_all_directories
from pipelines.extract_news import extract_news
from pipelines.transform_news import transform
from pipelines.upload_to_s3 import upload_to_s3


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pipelines'))

# Carregar variáveis do arquivo .env
load_dotenv()

default_args = {
    'owner': 'erick',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='etl_pipeline_diaria',
    default_args=default_args,
    description='Executa o ETL de notícias diariamente',
    schedule_interval='@daily',
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=['etl', 'news'],
) as dag:

    # Setup das pastas
    def setup_directories():
        directories = setup_all_directories()
        print(f"Diretórios preparados: {', '.join(directories.values())}")
        return "Diretórios preparados"
    
    setup_dirs = PythonOperator(
        task_id='setup_directories',
        python_callable=setup_directories,
    )

    # Tarefa de extração de notícias - CORRIGIDA
    extract_news_task = PythonOperator(
        task_id='extract_news',
        python_callable=extract_news,
        op_kwargs={
            'query': 'query',
            'from_date': '2025-01-01',
            'to_date': '2025-01-02'
        }
    )
    
    # Tarefa de transformação de notícias
    transform_news_task = PythonOperator(
        task_id='transform_news',
        python_callable=transform,
    )
    
    # Tarefa de upload para o S3
    upload_news = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
    )
    
    # Definindo a sequência de execução
    setup_dirs >> extract_news_task >> transform_news_task >> upload_news