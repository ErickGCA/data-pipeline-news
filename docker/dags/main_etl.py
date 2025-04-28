import json
import os
import datetime
import logging
from dotenv import load_dotenv
from extract_news import fetch_news
from transform_news import transform
from upload_to_s3 import upload_to_s3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def main_etl():
    logger.info("=" * 50)
    logger.info(f"Iniciando ETL em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    raw_path = os.path.join(raw_dir, "raw_news.json")
    processed_path = os.path.join(processed_dir, "processed_news.json")

    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            raise ValueError("Chave de API não encontrada. Configure a variável NEWS_API_KEY no arquivo .env")
        
        query = '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")'
        
        logger.info(f"Iniciando extração com a consulta: {query}")
        noticias = fetch_news(api_key, query, days_back=30)

        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(noticias, f, ensure_ascii=False, indent=4)
        logger.info(f"Extract finalizado com sucesso: {len(noticias)} notícias extraídas")
    except Exception as e:
        logger.error(f"Erro na etapa de Extract: {e}")
        return False

    try:
        transform(raw_path, processed_path)

        with open(processed_path, 'r', encoding='utf-8') as f:
            processed_data = json.load(f)

        logger.info(f"Transform finalizado com sucesso: {len(processed_data)} notícias relevantes identificadas")
    except Exception as e:
        logger.error(f"Erro na etapa de Transform: {e}")
        return False

    try:
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("Nome do bucket S3 não encontrado. Configure a variável S3_BUCKET_NAME no arquivo .env")
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        object_name_timestamped = f"processed_news_{timestamp}.json"
        
        upload_to_s3(processed_path, bucket_name, object_name_timestamped)
        upload_to_s3(processed_path, bucket_name, "processed_news_latest.json")

        logger.info(f"Load finalizado com sucesso: dados enviados para {bucket_name}/{object_name_timestamped}")
    except Exception as e:
        logger.error(f"Erro na etapa de Load: {e}")
        return False

    logger.info("=" * 50)
    logger.info(f"Pipeline ETL concluído com sucesso em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)
    return True

if __name__ == "__main__":
    main_etl()
