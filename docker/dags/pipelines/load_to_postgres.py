import os
import pandas as pd
import json
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def load_to_postgres(processed_news_path, raw_news_path):
    
    df_raw = pd.read_json(raw_news_path)
    df_processed = pd.read_json(processed_news_path)
    
    df_raw['source_name'] = df_raw['source'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
    df_raw['source_id'] = df_raw['source'].apply(lambda x: x.get('id') if isinstance(x, dict) else None)
    
    df_raw = df_raw.drop('source', axis=1)
    
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    assert all([user, password, host, port, db]), "Variáveis de ambiente faltando"

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
    
    df_raw.to_sql("raw_news", engine, index=False, if_exists="replace")
    df_processed.to_sql("processed_news", engine, index=False, if_exists="replace")
    
    return f"Successfully loaded {len(df_raw)} raw news items and {len(df_processed)} processed news items to PostgreSQL"