import requests
from datetime import datetime
from typing import Dict, Any, List, Optional

from src.etl.extractors.base_extractor import BaseExtractor
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("gnews_extractor")


class GNewsExtractor(BaseExtractor):
    """
    Extrator de notícias da API GNews.
    Implementa a interface BaseExtractor.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o extrator com a chave da API.
        
        Args:
            api_key: Chave da API GNews (opcional)
        """
        self.config = Config()
        self.api_key = api_key or self.config.gnews_api_key
    
    def extract(self, query: str, from_date: str, to_date: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Extrai notícias da GNews API.
        
        Args:
            query: Consulta para busca de notícias
            from_date: Data inicial no formato YYYY-MM-DD
            to_date: Data final no formato YYYY-MM-DD
            **kwargs: Parâmetros adicionais (language, country, max_results)
            
        Returns:
            List[Dict[str, Any]]: Lista de artigos extraídos
        """
        language = kwargs.get("language", "pt")
        country = kwargs.get("country", "br")
        max_results = kwargs.get("max_results", 20)
        
        if not self.validate_source():
            logger.error("API key inválida ou não configurada")
            return []
        
        logger.info(f"Buscando notícias da GNews de {from_date} até {to_date}...")
        
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
            from_timestamp = int(from_date_obj.timestamp())
        except ValueError:
            logger.error(f"Formato de data inválido para from_date: {from_date}")
            return []
        
        url = (
            f"https://gnews.io/api/v4/search?q={query}"
            f"&lang={language}&country={country}&max={max_results}"
            f"&from={from_date}T00:00:00Z&to={to_date}T23:59:59Z"
            f"&apikey={self.api_key}"
        )
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            articles = data.get("articles", [])
            
            standardized_articles = []
            for article in articles:
                standardized_article = {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "content": article.get("content"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt"),
                    "source": {
                        "name": article.get("source", {}).get("name"),
                        "url": article.get("source", {}).get("url")
                    },
                    "_source": "gnews"
                }
                standardized_articles.append(standardized_article)
            
            logger.info(f"{len(standardized_articles)} artigos encontrados na GNews de {from_date} até {to_date}")
            return standardized_articles
            
        except Exception as e:
            logger.error(f"Erro na extração da GNews para o período {from_date} a {to_date}: {e}")
            return []
    
    def validate_source(self) -> bool:
        """
        Valida se a chave da API está configurada.
        
        Returns:
            bool: True se a chave for válida, False caso contrário
        """
        return bool(self.api_key)
    
    def get_source_name(self) -> str:
        """
        Retorna o nome da fonte.
        
        Returns:
            str: Nome da fonte
        """
        return "GNews" 