from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os


from main_etl import main_etl  

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

    executar_etl = PythonOperator(
        task_id='executar_etl_news',
        python_callable=main_etl,  
    )

    executar_etl