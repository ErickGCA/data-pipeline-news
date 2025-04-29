import requests
import datetime
import logging

logger = logging.getLogger(__name__)

def fetch_news_window(api_key, query, from_date, to_date, language='pt', page_size=100):
    url = (
        f'https://newsapi.org/v2/everything?q={query}'
        f'&language={language}&pageSize={page_size}&page=1'
        f'&from={from_date}&to={to_date}&sortBy=relevancy&apiKey={api_key}'
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])
        logger.info(f"{len(articles)} artigos encontrados de {from_date} até {to_date}")
        return articles
    except Exception as e:
        logger.error(f"Erro na janela {from_date} a {to_date}: {e}")
        return []
