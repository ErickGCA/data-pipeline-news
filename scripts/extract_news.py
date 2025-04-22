# Corrigir posteriormente os paths (base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# file_path = os.path.join(base_dir, "data", "raw_news.json")
# os.makedirs(os.path.dirname(file_path), exist_ok=True))

import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_news(api_key, query, language='pt', page_size=100, max_pages=5):
    all_articles = []
    
    for page in range(1, max_pages + 1):
        url = (
            f'https://newsapi.org/v2/everything?q={query}'
            f'&language={language}&pageSize={page_size}&page={page}&apiKey={api_key}'
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                if not articles:
                    break
                all_articles.extend(articles)
            else:
                print(f"Erro na página {page}: {response.status_code}")
                break
        except Exception as e:
            print(f"Erro ao fazer requisição: {e}")
            break

    return all_articles

if __name__ == "__main__":
    api_key = os.getenv("NEWS_API_KEY")
    query = "acidente de carro com álcool"

    noticias = fetch_news(api_key, query)

    os.makedirs("../pipelines-news/data", exist_ok=True)
    with open('../pipelines-news/data/raw_news.json', 'w', encoding='utf-8') as f:
        json.dump(noticias, f, ensure_ascii=False, indent=4)


    # print("Salvando em:", os.path.abspath('../pipelines-news/data/raw_news.json'))

    print(f"{len(noticias)} notícias extraídas e salvas em 'raw_news.json'")
