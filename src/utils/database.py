from typing import Optional, Any
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("database")


class Database:
    """
    Classe para gerenciar conexões e operações com o banco de dados.
    Segue o padrão Singleton para garantir uma única instância de conexão.
    """
    
    _instance = None
    _engine = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.config = Config()
    
    @property
    def engine(self) -> Engine:
        """
        Retorna o engine de conexão com o banco de dados.
        Cria um novo engine se não existir.
        
        Returns:
            Engine: Engine de conexão SQLAlchemy
        """
        if self._engine is None:
            conn_string = self.config.get_postgres_conn_string()
            self._engine = create_engine(conn_string)
            logger.info("Engine de conexão com PostgreSQL criado")
        return self._engine
    
    def execute_query(self, query: str, params: Optional[dict] = None) -> Any:
        """
        Executa uma query SQL.
        
        Args:
            query: Query SQL a ser executada
            params: Parâmetros para a query (opcional)
            
        Returns:
            Any: Resultado da execução
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return result
        except Exception as e:
            logger.error(f"Erro ao executar query: {e}")
            raise
    
    def dataframe_to_sql(self, df: pd.DataFrame, table_name: str, if_exists: str = "replace", 
                          index: bool = False) -> bool:
        """
        Salva um DataFrame no banco de dados.
        
        Args:
            df: DataFrame a ser salvo
            table_name: Nome da tabela
            if_exists: Comportamento se a tabela existir ('fail', 'replace', 'append')
            index: Se deve incluir o índice do DataFrame
            
        Returns:
            bool: True se bem-sucedido, False caso contrário
        """
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=index)
            logger.info(f"DataFrame salvo na tabela {table_name} com {len(df)} registros")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar DataFrame na tabela {table_name}: {e}")
            return False
    
    def query_to_dataframe(self, query: str, params: Optional[dict] = None) -> pd.DataFrame:
        """
        Executa uma query e retorna os resultados como DataFrame.
        
        Args:
            query: Query SQL a ser executada
            params: Parâmetros para a query (opcional)
            
        Returns:
            pd.DataFrame: Resultados da query como DataFrame
        """
        try:
            return pd.read_sql(query, self.engine, params=params)
        except Exception as e:
            logger.error(f"Erro ao executar query para DataFrame: {e}")
            return pd.DataFrame() 