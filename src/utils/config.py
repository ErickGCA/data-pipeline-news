import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """
    Classe de configuração centralizada para toda a aplicação.
    Segue o padrão Singleton para garantir uma única instância.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        load_dotenv()
        
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.base_dir / "data"
        self.raw_data_dir = self.data_dir / "raw"
        self.processed_data_dir = self.data_dir / "processed"
        
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.gnews_api_key = os.getenv("GNEWS_API_KEY")
        self.newsdata_api_key = os.getenv("NEWSDATA_API_KEY")
        
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.postgres_host = os.getenv("POSTGRES_HOST", "localhost")
        self.postgres_port = os.getenv("POSTGRES_PORT", "5432")
        self.postgres_db = os.getenv("POSTGRES_DB", "airflow")
        
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = os.getenv("AWS_SECRET_KEY")
        self.s3_bucket = os.getenv("S3_BUCKET")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        self._initialized = True
    
    def get_postgres_conn_string(self) -> str:
        """
        Retorna a string de conexão para o PostgreSQL.
        
        Returns:
            str: String de conexão PostgreSQL
        """
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    def get_api_key(self, api_name: str) -> Optional[str]:
        """
        Retorna a chave de API específica.
        
        Args:
            api_name: Nome da API ('newsapi', 'gnews', 'newsdata')
            
        Returns:
            Optional[str]: Chave da API ou None se não encontrada
        """
        api_keys = {
            "newsapi": self.news_api_key,
            "gnews": self.gnews_api_key,
            "newsdata": self.newsdata_api_key
        }
        return api_keys.get(api_name.lower())
    
    def validate_required_env(self, keys: list) -> bool:
        """
        Valida se as variáveis de ambiente necessárias estão configuradas.
        
        Args:
            keys: Lista de chaves de ambiente a serem validadas
            
        Returns:
            bool: True se todas as chaves existirem, False caso contrário
        """
        for key in keys:
            value = getattr(self, key, None)
            if not value:
                return False
        return True 