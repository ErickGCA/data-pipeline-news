import requests
import logging

logger = logging.getLogger(__name__)

def fetch_newsdata(api_key, query, from_date, to_date, lang="pt", max_results=10):
    logger.info(f"Buscando notícias do NewsData.io...")

    simplified_query = "acidente álcool embriaguez lei seca"
    
    url = "https://newsdata.io/api/1/latest"
    params = {
        "q": simplified_query,
        "language": lang,
        "size": max_results,
        "apikey": api_key,
        "country": "br",
        "timezone": "America/Sao_Paulo"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "error":
            logger.error(f"Erro na API do NewsData.io: {data.get('results', {}).get('message')}")
            return []

        articles = data.get("results", [])

        formatted_articles = [
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "url": article.get("link"),
                "source": {"name": article.get("source_id")},
                "publishedAt": article.get("pubDate"),
            }
            for article in articles
        ]

        logger.info(f"{len(formatted_articles)} notícias extraídas do NewsData.io.")
        return formatted_articles

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar notícias do NewsData.io: {e}")
        if hasattr(e.response, 'text'):
            logger.error(f"Detalhes do erro: {e.response.text}")
        return [] 