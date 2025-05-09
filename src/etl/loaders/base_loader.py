from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseLoader(ABC):
    """
    Interface base para todos os carregadores de dados.
    Seguindo o princípio da Interface Segregation (ISP) do SOLID.
    """
    
    @abstractmethod
    def load(self, data: List[Dict[str, Any]], **kwargs) -> bool:
        """
        Método para carregar dados em um destino.
        
        Args:
            data: Lista de registros a serem carregados
            **kwargs: Parâmetros específicos para o carregamento
            
        Returns:
            bool: True se o carregamento for bem-sucedido, False caso contrário
        """
        pass
    
    @abstractmethod
    def validate_destination(self) -> bool:
        """
        Método para validar o destino dos dados.
        
        Returns:
            bool: True se o destino for válido, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_loader_name(self) -> str:
        """
        Retorna o nome do carregador.
        
        Returns:
            str: Nome do carregador
        """
        pass 