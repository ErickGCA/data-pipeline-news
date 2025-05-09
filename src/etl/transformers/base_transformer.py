from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseTransformer(ABC):
    """
    Interface base para todos os transformadores de dados.
    Seguindo o princípio da Interface Segregation (ISP) do SOLID.
    """
    
    @abstractmethod
    def transform(self, data: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """
        Método para transformar dados.
        
        Args:
            data: Lista de registros a serem transformados
            **kwargs: Parâmetros específicos para a transformação
            
        Returns:
            List[Dict[str, Any]]: Lista de registros transformados
        """
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Método para validar um registro.
        
        Args:
            data: Registro a ser validado
            
        Returns:
            bool: True se o registro for válido, False caso contrário
        """
        pass
    
    @abstractmethod
    def get_transformer_name(self) -> str:
        """
        Retorna o nome do transformador.
        
        Returns:
            str: Nome do transformador
        """
        pass 