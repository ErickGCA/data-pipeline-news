import requests
import json
import os
import datetime
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

load_dotenv()

def fetch_news(api_key, query, language='pt', page_size=100, max_pages=1, days_back=30):
    all_articles = []
    from_date = (datetime.datetime.now() - datetime.timedelta(days=days_back)).strftime('%Y-%m-%d')
    to_date = datetime.datetime.now().strftime('%Y-%m-%d')

    for page in range(1, max_pages + 1):
        url = (
            f'https://newsapi.org/v2/everything?q={query}'
            f'&language={language}&pageSize={page_size}&page={page}'
            f'&from={from_date}&to={to_date}&sortBy=relevancy&apiKey={api_key}'
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                total_results = data.get('totalResults', 0)

                if total_results > 100:
                    print(f"AVISO: A consulta retornou {total_results} resultados, mas apenas os primeiros 100 serão extraídos devido à limitação da API.")

                if not articles:
                    print(f"Nenhum artigo encontrado na página {page}")
                    break

                all_articles.extend(articles)
                print(f"Página {page}: {len(articles)} artigos encontrados")

                if len(all_articles) >= 100:
                    break

            else:
                print(f"Erro na página {page}: {response.status_code}, {response.text}")
                break
        except Exception as e:
            print(f"Erro ao fazer requisição: {e}")
            break

    return all_articles

if __name__ == "__main__":
    raw_news_path = os.path.join(data_dir, "raw_news.json")
    
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError("Chave de API não encontrada. Configure a variável NEWS_API_KEY no arquivo .env")
    
    query = '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")'
    
    print(f"Iniciando extração de notícias com a consulta: {query}")
    
    news = fetch_news(api_key, query)
    
    print(f"Total de {len(news)} notícias extraídas")
    
    with open(raw_news_path, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=4)
    
    print(f"Dados brutos salvos em: {raw_news_path}")