import requests
import json
import os
import datetime
import logging
from dotenv import load_dotenv
from utils.create_directory import create_directory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__)) 
data_dir = os.path.join(base_dir, "data/raw")  
create_directory(data_dir)

raw_news_path = os.path.join(data_dir, "raw_news.json")
load_dotenv()

def fetch_news(api_key, query, output_path=None, language='pt', page_size=100, max_pages=1, days_back=30):
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
                    logger.warning(f"AVISO: A consulta retornou {total_results} resultados, mas apenas os primeiros 100 serão extraídos devido à limitação da API.")

                if not articles:
                    logger.info(f"Nenhum artigo encontrado na página {page}")
                    break

                all_articles.extend(articles)
                logger.info(f"Página {page}: {len(articles)} artigos encontrados")

                if len(all_articles) >= 100:
                    break

            else:
                logger.error(f"Erro na página {page}: {response.status_code}, {response.text}")
                break
        except Exception as e:
            logger.error(f"Erro ao fazer requisição: {e}")
            break

    return all_articles

if __name__ == "__main__":
    raw_news_path = os.path.join(data_dir, "raw_news.json")
    
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError("Chave de API não encontrada. Configure a variável NEWS_API_KEY no arquivo .env")
    
    query = '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")'
    
    logger.info(f"Iniciando extração de notícias com a consulta: {query}")
    
    news = fetch_news(api_key, query)
    
    logger.info(f"Total de {len(news)} notícias extraídas")
    
    with open(raw_news_path, 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=4)
    
    logger.info(f"Dados brutos salvos em: {raw_news_path}")
