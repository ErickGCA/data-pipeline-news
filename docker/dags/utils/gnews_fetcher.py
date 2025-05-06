import requests
import logging

logger = logging.getLogger(__name__)

def fetch_gnews(api_key, query, from_date, to_date, lang="pt", max_results=100):
    logger.info(f"Buscando notícias da GNews de {from_date} até {to_date}...")

    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "lang": lang,
        "max": max_results,
        "apikey": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])

        formatted_articles = [
            {
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "url": article.get("url"),
                "source": article.get("source", {}).get("name"),
                "publishedAt": article.get("publishedAt"),
            }
            for article in articles
        ]

        logger.info(f"{len(formatted_articles)} notícias extraídas da GNews.")
        return formatted_articles

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar notícias da GNews: {e}")
        return []
