from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
from utils.setup_all_directories import setup_all_directories
from main_etl import main_etl

dag_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dag_dir)

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
    
    def setup_directories():
        directories = setup_all_directories()
        print(f"Diretórios preparados: {', '.join(directories.values())}")
        return "Diretórios preparados"
    
    setup_dirs = PythonOperator(
        task_id='setup_directories',
        python_callable=setup_directories,
    )
    
    executar_etl = PythonOperator(
        task_id='executar_etl_news',
        python_callable=main_etl,  
    )
    
    setup_dirs >> executar_etl