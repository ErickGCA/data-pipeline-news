from extract_news import fetch_news
from transform_news import transform
from upload_to_s3 import upload_to_s3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def run_etl():
    print("Iniciando ETL...")

    # Usar /tmp como diretório de escrita
    raw_path = "/tmp/raw_news.json"
    filtered_path = "/tmp/filtered_news.json"

    # Extract
    api_key = os.getenv("NEWS_API_KEY")
    query = "acidente de carro com álcool"
    noticias = fetch_news(api_key, query)
    
    with open(raw_path, 'w', encoding='utf-8') as f:
        json.dump(noticias, f, ensure_ascii=False, indent=4)
    print(f"Extract finalizado ({len(noticias)} notícias)")

    # Transform
    transform(raw_path, filtered_path)
    print("Transform finalizado")

    # Load
    bucket_name = os.getenv("S3_BUCKET_NAME")
    object_name = "filtered_news.json"
    upload_to_s3(filtered_path, bucket_name, object_name)
    print("Load finalizado")

