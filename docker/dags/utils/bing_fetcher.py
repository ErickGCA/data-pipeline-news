import requests
import logging

logger = logging.getLogger(__name__)

def fetch_bing(api_key, endpoint, query, from_date, to_date, count=100, market="pt-BR"):

    logger.info(f"Buscando notícias do Bing de {from_date} até {to_date}...")

    url = f"{endpoint}/bing/v7.0/news/search"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key
    }
    params = {
        "q": query,
        "count": count,
        "freshness": "Day",  
        "market": market,
        "sortBy": "Date"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        articles = data.get("value", [])

        formatted_articles = [
            {
                "title": article.get("name"),
                "description": article.get("description"),
                "content": None,  
                "url": article.get("url"),
                "source": article.get("provider", [{}])[0].get("name"),
                "publishedAt": article.get("datePublished"),
            }
            for article in articles
        ]

        logger.info(f"{len(formatted_articles)} notícias extraídas do Bing.")
        return formatted_articles

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar notícias no Bing: {e}")
        return []
