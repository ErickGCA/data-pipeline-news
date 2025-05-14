"""
DAG para ETL de notícias utilizando a arquitetura SOLID.
Esta DAG extrai notícias de múltiplas fontes, transforma-as para identificar
notícias relacionadas a acidentes com álcool, e carrega os resultados em
PostgreSQL e S3.
"""
import json
import sys
import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

sys.path.insert(0, "/opt/airflow")

from src.etl.extractors.news_api_extractor import NewsAPIExtractor
from src.etl.extractors.gnews_extractor import GNewsExtractor
from src.etl.transformers.news_transformer import NewsTransformer
from src.etl.loaders.postgres_loader import PostgresLoader
from src.etl.loaders.s3_uploader import S3Uploader
from src.utils.logger import setup_logger
from src.utils.config import Config

logger = setup_logger("news_etl_dag")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

config = Config()

NEWS_QUERY = '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")'


def extract_news(**kwargs):
    """
    Extrai notícias de múltiplas fontes
    """
    execution_date = kwargs['execution_date']
    days_back = kwargs.get('days_back', 2)
    
    end_date = execution_date.strftime('%Y-%m-%d')
    start_date = (execution_date - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    logger.info(f"Iniciando extração de notícias de {start_date} até {end_date}")
    
    news_api_extractor = NewsAPIExtractor()
    gnews_extractor = GNewsExtractor()
    
    news_api_articles = news_api_extractor.extract(
        query=NEWS_QUERY,
        from_date=start_date,
        to_date=end_date,
        language="pt"
    )
    
    gnews_articles = gnews_extractor.extract(
        query=NEWS_QUERY,
        from_date=start_date,
        to_date=end_date,
        language="pt",
        country="br"
    )
    
    all_articles = news_api_articles + gnews_articles
    
    logger.info(f"Extraídos {len(all_articles)} artigos no total")
    logger.info(f"- NewsAPI: {len(news_api_articles)} artigos")
    logger.info(f"- GNews: {len(gnews_articles)} artigos")
    
    extraction_metadata = {
        "start_date": start_date,
        "end_date": end_date,
        "total_articles": len(all_articles),
        "sources": {
            "newsapi": len(news_api_articles),
            "gnews": len(gnews_articles)
        }
    }
    
    return {
        "articles": all_articles,
        "metadata": extraction_metadata
    }

def transform_news(**kwargs):
    """
    Transforma notícias extraídas
    """
    ti = kwargs['ti']
    extraction_result = ti.xcom_pull(task_ids='extract_news')
    
    if not extraction_result or 'articles' not in extraction_result:
        logger.error("Nenhum artigo recebido para transformação")
        return None
    
    articles = extraction_result['articles']
    extraction_metadata = extraction_result['metadata']
    
    logger.info(f"Iniciando transformação de {len(articles)} artigos")
    
    transformer = NewsTransformer()
    
    transformed_articles = transformer.transform(
        data=articles,
        deduplicate=True
    )
    
    logger.info(f"Transformação concluída: {len(transformed_articles)} artigos relevantes identificados")
    
    transform_metadata = {
        "original_count": len(articles),
        "transformed_count": len(transformed_articles),
        "extraction_metadata": extraction_metadata
    }
    
    return {
        "articles": transformed_articles,
        "metadata": transform_metadata
    }

def load_to_postgres(**kwargs):
    """
    Carrega notícias transformadas no PostgreSQL
    """
    ti = kwargs['ti']
    transform_result = ti.xcom_pull(task_ids='transform_news')
    
    if not transform_result or 'articles' not in transform_result:
        logger.error("Nenhum artigo recebido para carregamento no PostgreSQL")
        return False
    
    articles = transform_result['articles']
    
    logger.info(f"Iniciando carregamento de {len(articles)} artigos no PostgreSQL")
    
    postgres_loader = PostgresLoader()
    
    result = postgres_loader.load(
        data=articles,
        table_name="news_data.processed_news",
        if_exists="append"
    )
    
    if result:
        logger.info("Carregamento no PostgreSQL concluído com sucesso")
    else:
        logger.error("Falha no carregamento no PostgreSQL")
    
    return result

def upload_to_s3(**kwargs):
    """
    Carrega notícias transformadas no S3
    """
    ti = kwargs['ti']
    transform_result = ti.xcom_pull(task_ids='transform_news')
    
    if not transform_result or 'articles' not in transform_result:
        logger.error("Nenhum artigo recebido para upload no S3")
        return False
    
    articles = transform_result['articles']
    metadata = transform_result['metadata']
    
    logger.info(f"Iniciando upload de {len(articles)} artigos para S3")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    object_name = f"processed_news_{timestamp}.json"
    
    s3_uploader = S3Uploader()
    
    result = s3_uploader.load(
        data=articles,
        object_name=object_name,
        metadata=metadata
    )
    
    if result:
        logger.info(f"Upload para S3 concluído com sucesso: {object_name}")
    else:
        logger.error("Falha no upload para S3")
    
    return result

with DAG(
    dag_id="news_etl_pipeline",
    default_args=default_args,
    description="ETL Pipeline para extração e análise de notícias sobre acidentes com álcool",
    schedule_interval="0 8 * * *",  # Diariamente às 8:00
    start_date=days_ago(1),
    catchup=False,
    tags=["news", "etl", "solid"],
) as dag:
    
    task_extract = PythonOperator(
        task_id="extract_news",
        python_callable=extract_news,
        provide_context=True,
        op_kwargs={"days_back": 2}
    )
    
    task_transform = PythonOperator(
        task_id="transform_news",
        python_callable=transform_news,
        provide_context=True
    )
    
    task_load_postgres = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres,
        provide_context=True
    )
    
    task_upload_s3 = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3,
        provide_context=True
    )
    
    task_extract >> task_transform >> [task_load_postgres, task_upload_s3] 