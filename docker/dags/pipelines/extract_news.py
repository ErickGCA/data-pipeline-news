
#extract_news.py

import os
import json
import logging
import datetime
from dotenv import load_dotenv
from utils.setup_all_directories import setup_all_directories
from utils.news_fetcher import fetch_news_window
from utils.deduplication import deduplicate_articles

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("NEWS_API_KEY")
    logger.info("")
    if not api_key:
        raise ValueError("Chave de API não encontrada. Configure a variável NEWS_API_KEY no arquivo .env")

    directories = setup_all_directories()
    raw_data_dir = directories["raw_data_dir"]
    raw_news_path = os.path.join(raw_data_dir, "raw_news.json")

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

        articles = fetch_news_window(api_key, query, from_date_str, to_date_str)
        all_articles.extend(articles)

        start_date = end_date

    logger.info(f"Total bruto de {len(all_articles)} notícias extraídas")

    unique_articles = deduplicate_articles(all_articles)

    mock_news_path = os.path.join(directories["mock_data_dir"], "mock_news_data.json")
    with open(mock_news_path, "w", encoding="utf-8") as f:
        json.dump(unique_articles, f, ensure_ascii=False, indent=4)
    logger.info(f"Total de {len(unique_articles)} notícias após deduplicação (salvo mock)")

    with open(raw_news_path, 'w', encoding='utf-8') as f:
        json.dump(unique_articles, f, ensure_ascii=False, indent=4)
    logger.info(f"Dados brutos salvos em: {raw_news_path}")

