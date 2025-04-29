def deduplicate_articles(articles):
    seen_urls = set()
    unique_articles = []
    
    for article in articles:
        url = article.get('url')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    
    return unique_articles
