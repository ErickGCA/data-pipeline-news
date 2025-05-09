import pandas as pd
from typing import Dict, Any, List, Optional

from src.etl.loaders.base_loader import BaseLoader
from src.utils.database import Database
from src.utils.logger import setup_logger

logger = setup_logger("postgres_loader")


class PostgresLoader(BaseLoader):
    """
    Carregador de dados para o PostgreSQL.
    Implementa a interface BaseLoader.
    """
    
    def __init__(self, table_name: Optional[str] = None):
        """
        Inicializa o carregador com o nome da tabela padrão.
        
        Args:
            table_name: Nome da tabela padrão (opcional)
        """
        self.db = Database()
        self.default_table_name = table_name
    
    def load(self, data: List[Dict[str, Any]], **kwargs) -> bool:
        """
        Carrega dados em uma tabela do PostgreSQL.
        
        Args:
            data: Lista de registros a serem carregados
            **kwargs: Parâmetros adicionais (table_name, if_exists, index)
            
        Returns:
            bool: True se o carregamento for bem-sucedido, False caso contrário
        """
        if not data:
            logger.warning("Nenhum dado para carregar no PostgreSQL")
            return False
        
        if not self.validate_destination():
            logger.error("Conexão com PostgreSQL não disponível")
            return False
        
        table_name = kwargs.get("table_name", self.default_table_name)
        if_exists = kwargs.get("if_exists", "replace")
        index = kwargs.get("index", False)
        
        if not table_name:
            logger.error("Nome da tabela não especificado")
            return False
        
        try:
            df = pd.DataFrame(data)
            
            for column in df.columns:
                if df[column].dtype == 'object':
                    if all(isinstance(x, dict) for x in df[column].dropna()):
                        for key in data[0][column].keys():
                            df[f"{column}_{key}"] = df[column].apply(
                                lambda x: x.get(key) if isinstance(x, dict) else None
                            )
                        df = df.drop(column, axis=1)
            
            result = self.db.dataframe_to_sql(
                df, table_name, if_exists=if_exists, index=index
            )
            
            if result:
                logger.info(f"Carregados {len(df)} registros na tabela {table_name}")
            else:
                logger.error(f"Falha ao carregar dados na tabela {table_name}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados no PostgreSQL: {e}")
            return False
    
    def validate_destination(self) -> bool:
        """
        Valida se a conexão com o PostgreSQL está disponível.
        
        Returns:
            bool: True se o PostgreSQL estiver disponível, False caso contrário
        """
        try:
            self.db.execute_query("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Erro ao validar conexão com PostgreSQL: {e}")
            return False
    
    def get_loader_name(self) -> str:
        """
        Retorna o nome do carregador.
        
        Returns:
            str: Nome do carregador
        """
        return "PostgresLoader" 