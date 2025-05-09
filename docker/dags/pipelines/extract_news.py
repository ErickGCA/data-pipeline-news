#extract_news.py

import os
import json
import logging
import datetime
from dotenv import load_dotenv
from utils.setup_all_directories import setup_all_directories
from utils.news_fetcher import fetch_news_window
from utils.deduplication import deduplicate_articles
from utils.gnews_fetcher import fetch_gnews
from utils.newsdata_fetcher import fetch_newsdata
from utils.data_lake_config import DataLakeConfig
#from utils.bing_fetcher import fetch_bing

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    load_dotenv()
    """
    bing_endpoint = os.getenv("BING_ENDPOINT")
    if not bing_endpoint:
        raise ValueError("Configure a variável BING_ENDPOINT no .env")
    """
    
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError("Chave de API não encontrada. Configure a variável NEWS_API_KEY no arquivo .env")
    
    gnews_api_key = os.getenv("GNEWS_API_KEY")
    if not gnews_api_key:
        print(gnews_api_key)
        raise ValueError("Chave de API não encontrada. Configure a variável GNEWS_API_KEY no arquivo .env")

    newsdata_api_key = os.getenv("NEWSDATA_API_KEY")
    if not newsdata_api_key:
        raise ValueError("Chave de API não encontrada. Configure a variável NEWSDATA_API_KEY no arquivo .env")
    """
    bing_api_key = os.getenv("BING_API_KEY")
    if not bing_api_key:
        raise ValueError("Chave de API não encontrada. Configure a variável BING_API_KEY no arquivo .env")
    """
    
    # Configuração do Data Lake
    directories = setup_all_directories()
    data_lake = DataLakeConfig(directories["data_dir"])
    
    # Timestamp para os arquivos
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    query = '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")'
    logger.info(f"Iniciando extração de notícias com a consulta: {query}")

    now = datetime.datetime.now()
    days_back = 2
    delta = datetime.timedelta(days=2)

    all_articles = []
    start_date = now - datetime.timedelta(days=days_back)

    while start_date < now:
        end_date = start_date + delta
        if end_date > now:
            end_date = now

        from_date_str = start_date.strftime('%Y-%m-%d')
        to_date_str = end_date.strftime('%Y-%m-%d')

        # Coleta de notícias por fonte
        newsapi_articles = fetch_news_window(api_key, query, from_date_str, to_date_str)
        gnews_articles = fetch_gnews(gnews_api_key, query, from_date_str, to_date_str)
        newsdata_articles = fetch_newsdata(newsdata_api_key, query, from_date_str, to_date_str)

        # Adiciona metadados de fonte
        for article in newsapi_articles:
            article["_source"] = "newsapi"
        for article in gnews_articles:
            article["_source"] = "gnews"
        for article in newsdata_articles:
            article["_source"] = "newsdata"

        all_articles.extend(newsapi_articles)
        all_articles.extend(gnews_articles)
        all_articles.extend(newsdata_articles)

        start_date = end_date

    logger.info(f"Total bruto de {len(all_articles)} notícias extraídas")

    # Salva notícias brutas com metadados
    raw_metadata = {
        "query": query,
        "date_range": {
            "start": from_date_str,
            "end": to_date_str
        },
        "sources": {
            "newsapi": len(newsapi_articles),
            "gnews": len(gnews_articles),
            "newsdata": len(newsdata_articles)
        }
    }
    
    raw_filename = f"raw_news_{timestamp}.json"
    data_lake.save_with_metadata(
        all_articles,
        "raw",
        raw_filename,
        raw_metadata
    )

    # Deduplicação
    unique_articles = deduplicate_articles(all_articles)
    
    # Salva notícias processadas com metadados
    processed_metadata = {
        "original_file": raw_filename,
        "deduplication_stats": {
            "total_articles": len(all_articles),
            "unique_articles": len(unique_articles),
            "duplicate_ratio": 1 - (len(unique_articles) / len(all_articles))
        }
    }
    
    processed_filename = f"processed_news_{timestamp}.json"
    data_lake.save_with_metadata(
        unique_articles,
        "processed",
        processed_filename,
        processed_metadata
    )

    logger.info(f"Pipeline concluído. {len(unique_articles)} notícias únicas processadas.")



