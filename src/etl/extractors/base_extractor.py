from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseExtractor(ABC):
    """
    Interface base para todos os extratores de dados.
    Seguindo o princípio da Interface Segregation (ISP) do SOLID.
    """
    
    @abstractmethod
    def extract(self, query: str, from_date: str, to_date: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Método para extrair dados de uma fonte.
        
        Args:
            query: Consulta para busca de notícias
            from_date: Data inicial no formato YYYY-MM-DD
            to_date: Data final no formato YYYY-MM-DD
            **kwargs: Parâmetros específicos para a extração
            
        Returns:
            List[Dict[str, Any]]: Lista de artigos extraídos
        """
        pass
    
    @abstractmethod
    def validate_source(self) -> bool:
        """
        Método para validar a disponibilidade e autenticidade da fonte.
        
        Returns:
            bool: True se a fonte for válida, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """
        Retorna o nome da fonte de dados.
        
        Returns:
            str: Nome da fonte
        """
        pass 