#trabalhar posteriormente com o salvamento no postgres

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime

def insert_news_to_postgres(**kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='postgres_conn') 
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO news (title, description, url, published_at, source_name, source_url)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    data = (
        'Notícia de exemplo',
        'Descrição de exemplo',
        'http://exemplo.com',
        datetime.now(),
        'Fonte de exemplo',
        'http://fonte.com'
    )
    cursor.execute(insert_query, data)
    conn.commit()

    cursor.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2025, 1, 1),
}

dag = DAG(
    'news_etl_to_postgres',
    default_args=default_args,
    description='ETL para inserir notícias no PostgreSQL',
    schedule_interval='@daily',
)

insert_news_task = PythonOperator(
    task_id='insert_news_to_postgres',
    python_callable=insert_news_to_postgres,
    provide_context=True,
    dag=dag,
)

insert_news_task
