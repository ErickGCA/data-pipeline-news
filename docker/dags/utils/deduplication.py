import logging
from difflib import SequenceMatcher
import re
from datetime import datetime

logger = logging.getLogger(__name__)

def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def similar(a, b, threshold=0.85):
    return SequenceMatcher(None, a, b).ratio() > threshold

def parse_date(date_str):
    if not date_str:
        return None
    try:
        formats = [
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d'
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None
    except Exception:
        return None

def deduplicate_articles(articles, similarity_threshold=0.85):
    """
    Remove artigos duplicados usando múltiplos critérios:
    1. URL exata
    2. Título similar
    3. Conteúdo similar
    4. Data de publicação próxima
    """
    if not articles:
        return []

    articles.sort(
        key=lambda x: parse_date(x.get("publishedAt")) or datetime.min,
        reverse=True
    )

    unique_articles = []
    seen_urls = set()
    seen_titles = set()

    for article in articles:
        url = article.get("url")
        title = article.get("title")
        content = article.get("content", "")
        published_at = parse_date(article.get("publishedAt"))

        norm_title = normalize_text(title) if title else ""
        norm_content = normalize_text(content)

        if url in seen_urls:
            logger.debug(f"Artigo duplicado por URL: {url}")
            continue

        is_title_duplicate = False
        for seen_title in seen_titles:
            if similar(norm_title, seen_title, similarity_threshold):
                is_title_duplicate = True
                logger.debug(f"Artigo duplicado por título similar: {title}")
                break

        if is_title_duplicate:
            continue

        seen_urls.add(url)
        seen_titles.add(norm_title)
        unique_articles.append(article)

    logger.info(f"Artigos reduzidos de {len(articles)} para {len(unique_articles)} após deduplicação")
    return unique_articles
