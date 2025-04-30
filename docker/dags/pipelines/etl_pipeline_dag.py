import json
import logging
import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from pipelines.transform_news import transform
from pipelines.upload_to_s3 import upload_to_s3
from utils.deduplication import deduplicate_articles
from utils.news_fetcher import fetch_news_window
from utils.setup_all_directories import setup_all_directories

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pipelines"))

directories = setup_all_directories()
raw_data_dir = directories["raw_data_dir"]
raw_news_path = os.path.join(raw_data_dir, "raw_news.json")
processed_news_path = os.path.join(
    directories["processed_data_dir"], "processed_news.json"
)
mock_data_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "mock_data",
    "mock_news_data.json",
)

load_dotenv()

default_args = {
    "owner": "erick",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


def extract_news_with_windows_and_fallback(**kwargs):
    api_key = kwargs.get("api_key")
    query = kwargs.get("query")
    days_back = kwargs.get("days_back", 7)
    delta_days = kwargs.get("delta_days", 2)
    logger.info(f"Iniciando extração de notícias com a consulta: {query}")

    try:
        now = datetime.now()
        delta = timedelta(days=delta_days)

        all_articles = []
        start_date = now - timedelta(days=days_back)

        while start_date < now:
            end_date = start_date + delta
            if end_date > now:
                end_date = now

            from_date_str = start_date.strftime("%Y-%m-%d")
            to_date_str = end_date.strftime("%Y-%m-%d")

            logger.info(f"Consultando janela de {from_date_str} até {to_date_str}")
            articles = fetch_news_window(api_key, query, from_date_str, to_date_str)
            all_articles.extend(articles)

            start_date = end_date

        logger.info(f"Total bruto de {len(all_articles)} notícias extraídas")

        if len(all_articles) == 0:
            raise Exception("API retornou zero notícias em todas as janelas de tempo")

        unique_articles = deduplicate_articles(all_articles)
        logger.info(f"Total de {len(unique_articles)} notícias após deduplicação")

        with open(raw_news_path, "w", encoding="utf-8") as f:
            json.dump(unique_articles, f, ensure_ascii=False, indent=4)

        os.makedirs(os.path.dirname(mock_data_path), exist_ok=True)
        with open(mock_data_path, "w", encoding="utf-8") as f:
            json.dump(unique_articles, f, ensure_ascii=False, indent=4)

        return f"Extração concluída com sucesso: {len(unique_articles)} notícias únicas extraídas"

    except Exception as e:
        logger.warning(f"Erro na extração de notícias: {e}")
        logger.warning("Utilizando dados de mock como fallback")

        if not os.path.exists(mock_data_path):
            logger.error("Arquivo de mock não encontrado. Falha na extração.")
            raise

        with open(mock_data_path, "r", encoding="utf-8") as f:
            noticias_mock = json.load(f)

        logger.info(f"Carregados {len(noticias_mock)} notícias do arquivo de mock")

        with open(raw_news_path, "w", encoding="utf-8") as f:
            json.dump(noticias_mock, f, ensure_ascii=False, indent=4)

        return f"Extração realizada utilizando dados de mock (fallback): {len(noticias_mock)} notícias"


with DAG(
    dag_id="etl_pipeline_diaria",
    default_args=default_args,
    description="Executa o ETL de notícias diariamente",
    schedule_interval="@daily",
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=["etl", "news"],
) as dag:

    def setup_directories():
        logger.info(f"Diretórios preparados: {', '.join(directories.values())}")
        return "Diretórios preparados"

    setup_dirs = PythonOperator(
        task_id="setup_directories",
        python_callable=setup_directories,
    )

    extract_news_task = PythonOperator(
        task_id="extract_news",
        python_callable=extract_news_with_windows_and_fallback,
        op_kwargs={
            "api_key": os.getenv("NEWS_API_KEY"),
            "query": '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")',
            "days_back": 7,
            "delta_days": 2,
        },
    )

    transform_news_task = PythonOperator(
        task_id="transform_news",
        python_callable=transform,
        op_args=[raw_news_path, processed_news_path],
    )

    def upload_with_timestamp(**kwargs):
        bucket_name = kwargs.get("bucket_name")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        object_name_timestamped = f"processed_news_{timestamp}.json"
        upload_to_s3(processed_news_path, bucket_name, object_name_timestamped)

        upload_to_s3(processed_news_path, bucket_name, "processed_news_latest.json")

        logger.info(
            f"Dados enviados para {bucket_name}/{object_name_timestamped} e processed_news_latest.json"
        )

        return "Upload para S3 concluído"

    upload_news = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_with_timestamp,
        op_kwargs={"bucket_name": os.getenv("S3_BUCKET_NAME")},
    )

    setup_dirs >> extract_news_task >> transform_news_task >> upload_news
