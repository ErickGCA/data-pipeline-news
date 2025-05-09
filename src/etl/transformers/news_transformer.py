import re
import unicodedata
from typing import Dict, Any, List, Set

from src.etl.transformers.base_transformer import BaseTransformer
from src.utils.logger import setup_logger

logger = setup_logger("news_transformer")


class NewsTransformer(BaseTransformer):
    """
    Transformador de notícias relacionadas a acidentes com álcool.
    Implementa a interface BaseTransformer.
    """
    
    def __init__(self):
        """
        Inicializa o transformador.
        """
        pass
    
    def transform(self, data: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """
        Transforma e filtra notícias relacionadas a acidentes com álcool.
        
        Args:
            data: Lista de notícias a serem transformadas
            **kwargs: Parâmetros adicionais
            
        Returns:
            List[Dict[str, Any]]: Lista de notícias transformadas e filtradas
        """
        filtered_news = []
        
        if kwargs.get("deduplicate", True):
            data = self._deduplicate_articles(data)
            
        for article in data:
            content = f"{article.get('title', '')} {article.get('description', '')} {article.get('content', '')}"
            
            if self._is_alcohol_accident(content):
                relevance_score = self._calculate_relevance(content)
                
                transformed_article = {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "publishedAt": article.get("publishedAt"),
                    "relevance_score": relevance_score,
                    "source": article.get("source", {}).get("name") if isinstance(article.get("source"), dict) else article.get("source"),
                    "original_source": article.get("_source", "unknown")
                }
                
                filtered_news.append(transformed_article)
        
        filtered_news.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        logger.info(f"Transformadas {len(filtered_news)} notícias relevantes de um total de {len(data)}")
        return filtered_news
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Valida se um registro tem os campos mínimos necessários.
        
        Args:
            data: Registro a ser validado
            
        Returns:
            bool: True se o registro for válido, False caso contrário
        """
        required_fields = ["title", "url"]
        return all(field in data for field in required_fields)
    
    def get_transformer_name(self) -> str:
        """
        Retorna o nome do transformador.
        
        Returns:
            str: Nome do transformador
        """
        return "NewsTransformer"
    
    def _normalize_text(self, text: str) -> str:
        """
        Normaliza o texto removendo acentos e convertendo para minúsculas.
        
        Args:
            text: Texto a ser normalizado
            
        Returns:
            str: Texto normalizado
        """
        if not text:
            return ""
        text = text.lower()
        return "".join(
            c for c in unicodedata.normalize("NFD", text) 
            if unicodedata.category(c) != "Mn"
        )
    
    def _is_alcohol_accident(self, text: str) -> bool:
        """
        Verifica se o texto contém indicações de acidente relacionado a álcool.
        
        Args:
            text: Texto a ser analisado
            
        Returns:
            bool: True se for um acidente relacionado a álcool, False caso contrário
        """
        text = text.lower()

        keywords = [
            r"acidente.*(álcool|alcool|bebida|embriagado|embriaguez)",
            r"embriagado|embriaguez",
            r"(dirigia|conduzia|ao volante).*(bêbado|bebado|alcoolizado|embriagado)",
            r"(motorista|condutor).*(bêbado|bebado|alcoolizado|embriagado)",
            r"sob (efeito|influência).*(álcool|alcool|bebida)",
            r"(teste|exame).*(alcoolemia|etilômetro|bafômetro)",
            r"lei seca.*(acidente|colisão|batida|capotamento|atropelamento)",
            r"(álcool|alcool|bebida).*(volante|direção)",
            r"(capotamento|colisão|batida|acidente).*(álcool|alcool|embriaguez)",
            r"(vítima|vitima|morto|ferido).*(motorista|condutor).*(bêbado|bebado|alcoolizado|embriagado)",
        ]

        norm_text = self._normalize_text(text)
        norm_keywords = [
            r"acidente.*(alcool|bebida|embriagado|embriaguez)",
            r"embriagado|embriaguez",
            r"(dirigia|conduzia|ao volante).*(bebado|alcoolizado|embriagado)",
            r"(motorista|condutor).*(bebado|alcoolizado|embriagado)",
            r"sob (efeito|influencia).*(alcool|bebida)",
            r"(teste|exame).*(alcoolemia|etilometro|bafometro)",
            r"lei seca.*(acidente|colisao|batida|capotamento|atropelamento)",
            r"(alcool|bebida).*(volante|direcao)",
            r"(capotamento|colisao|batida|acidente).*(alcool|embriaguez)",
            r"(vitima|morto|ferido).*(motorista|condutor).*(bebado|alcoolizado|embriagado)",
        ]

        return any(re.search(kw, text) for kw in keywords) or any(
            re.search(kw, norm_text) for kw in norm_keywords
        )
    
    def _calculate_relevance(self, text: str) -> int:
        """
        Calcula um score de relevância para o texto.
        
        Args:
            text: Texto para calcular relevância
            
        Returns:
            int: Score de relevância
        """
        text = text.lower()
        score = 0

        primary_patterns = [
            r"(dirigia|conduzia|ao volante).*(bêbado|bebado|alcoolizado|embriagado)",
            r"(motorista|condutor).*(bêbado|bebado|alcoolizado|embriagado)",
            r"sob (efeito|influência) de (álcool|alcool)",
            r"(teste|exame).*(alcoolemia|etilômetro|bafômetro).*(positivo|acima)",
            r"lei seca.*(infração|infracao|autuado|detido)",
        ]

        secondary_patterns = [
            r"(acidente|colisão|batida).*(álcool|alcool)",
            r"lei seca",
            r"(bafômetro|etilômetro)",
            r"(embriagado|embriaguez)",
            r"(vítima|vitima|morto|ferido).*(álcool|alcool)",
        ]

        tertiary_patterns = [
            r"acidente",
            r"álcool|alcool",
            r"colisão|batida",
            r"motorista|condutor",
        ]

        for pattern in primary_patterns:
            if re.search(pattern, text):
                score += 3

        for pattern in secondary_patterns:
            if re.search(pattern, text):
                score += 2

        for pattern in tertiary_patterns:
            if re.search(pattern, text):
                score += 1

        return score
    
    def _deduplicate_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove artigos duplicados baseados no título ou URL.
        
        Args:
            articles: Lista de artigos a serem deduplicados
            
        Returns:
            List[Dict[str, Any]]: Lista de artigos únicos
        """
        unique_articles = []
        seen_titles: Set[str] = set()
        seen_urls: Set[str] = set()
        
        for article in articles:
            title = self._normalize_text(article.get("title", ""))
            url = article.get("url", "").strip()
            
            if title and url and title not in seen_titles and url not in seen_urls:
                seen_titles.add(title)
                seen_urls.add(url)
                unique_articles.append(article)
        
        logger.info(f"Deduplicados {len(articles) - len(unique_articles)} artigos duplicados")
        return unique_articles 