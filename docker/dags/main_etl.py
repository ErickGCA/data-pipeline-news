from extract_news import fetch_news
from transform_news import transform
from upload_to_s3 import upload_to_s3
import json
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

def main_etl():
   
   
    #print(f"Diretório de trabalho atual: {os.getcwd()}")

    print("=" * 50)
    print(f"Iniciando ETL em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    raw_path = os.path.join(data_dir, "raw_news.json")
    filtered_path = os.path.join(data_dir, "filtered_news.json")

    #print(f"Diretório base: {base_dir}")
    #print(f"Diretório de dados: {data_dir}")
    #print(f"Caminho raw_news: {raw_path}")
    #print(f"Caminho filtered_news: {filtered_path}")

    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            raise ValueError("Chave de API não encontrada. Configure a variável NEWS_API_KEY no arquivo .env")
        
        query = '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")'
        
        print(f"Iniciando extração com a consulta: {query}")
        noticias = fetch_news(api_key, query, days_back=30)  

        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(noticias, f, ensure_ascii=False, indent=4)
        print(f"Extract finalizado com sucesso: {len(noticias)} notícias extraídas")
    except Exception as e:
        print(f"Erro na etapa de Extract: {e}")
        return False

    try:
        transform(raw_path, filtered_path)
        
        with open(filtered_path, 'r', encoding='utf-8') as f:
            filtered_data = json.load(f)
        
        print(f"Transform finalizado com sucesso: {len(filtered_data)} notícias relevantes identificadas")
    except Exception as e:
        print(f"Erro na etapa de Transform: {e}")
        return False

    try:
        bucket_name = os.getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("Nome do bucket S3 não encontrado. Configure a variável S3_BUCKET_NAME no arquivo .env")
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        object_name = f"filtered_news_{timestamp}.json"
        
        upload_to_s3(filtered_path, bucket_name, object_name)
        upload_to_s3(filtered_path, bucket_name, "filtered_news_latest.json")
        
        print(f"Load finalizado com sucesso: dados enviados para {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Erro na etapa de Load: {e}")
        return False

    print("=" * 50)
    print(f"Pipeline ETL concluído com sucesso em {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    return True

if __name__ == "__main__":
    main_etl()