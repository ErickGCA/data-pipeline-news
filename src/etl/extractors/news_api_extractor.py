import requests
from typing import Dict, Any, List, Optional

from src.etl.extractors.base_extractor import BaseExtractor
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("news_api_extractor")


class NewsAPIExtractor(BaseExtractor):
    """
    Extrator de notícias da API News API.
    Implementa a interface BaseExtractor.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o extrator com a chave da API.
        
        Args:
            api_key: Chave da API News API (opcional)
        """
        self.config = Config()
        self.api_key = api_key or self.config.news_api_key
    
    def extract(self, query: str, from_date: str, to_date: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Extrai notícias da News API.
        
        Args:
            query: Consulta para busca de notícias
            from_date: Data inicial no formato YYYY-MM-DD
            to_date: Data final no formato YYYY-MM-DD
            **kwargs: Parâmetros adicionais (language, page_size)
            
        Returns:
            List[Dict[str, Any]]: Lista de artigos extraídos
        """
        language = kwargs.get("language", "pt")
        page_size = kwargs.get("page_size", 50)
        
        if not self.validate_source():
            logger.error("API key inválida ou não configurada")
            return []
        
        logger.info(f"Buscando notícias da NewsAPI de {from_date} até {to_date}...")

        url = (
            f"https://newsapi.org/v2/everything?q={query}"
            f"&language={language}&pageSize={page_size}&page=1"
            f"&from={from_date}&to={to_date}&sortBy=relevancy&apiKey={self.api_key}"
        )
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            
            for article in articles:
                article["_source"] = "newsapi"
                
            logger.info(f"{len(articles)} artigos encontrados de {from_date} até {to_date}")
            return articles
            
        except Exception as e:
            logger.error(f"Erro na extração da NewsAPI para o período {from_date} a {to_date}: {e}")
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
        return "NewsAPI" 