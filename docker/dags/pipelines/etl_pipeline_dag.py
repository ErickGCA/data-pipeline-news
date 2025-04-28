from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

dag_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dag_dir)

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

    def setup_directories():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        print(f"Diretório criado: {data_dir}")
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