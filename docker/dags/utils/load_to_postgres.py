import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def load_to_postgres(processed_news_path):
    
    df = pd.read_json(processed_news_path)
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    assert all([user, password, host, port, db]), "Variáveis de ambiente faltando"

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")
    df.to_sql("noticias", engine, index=False, if_exists="replace")