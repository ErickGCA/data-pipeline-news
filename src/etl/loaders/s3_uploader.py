import boto3
import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from botocore.exceptions import ClientError

from src.etl.loaders.base_loader import BaseLoader
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("s3_uploader")


class S3Uploader(BaseLoader):
    """
    Carregador de dados para o Amazon S3.
    Implementa a interface BaseLoader.
    """
    
    def __init__(self, bucket_name: Optional[str] = None, region_name: Optional[str] = None):
        """
        Inicializa o uploader com nome do bucket e região.
        
        Args:
            bucket_name: Nome do bucket S3 (opcional)
            region_name: Nome da região AWS (opcional)
        """
        self.config = Config()
        self.bucket_name = bucket_name or self.config.s3_bucket
        self.region_name = region_name or self.config.aws_region
        self._s3_client = None
    
    @property
    def s3_client(self):
        """
        Retorna cliente S3, criando um novo se não existir.
        
        Returns:
            boto3.client: Cliente S3
        """
        if self._s3_client is None:
            try:
                self._s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=self.config.aws_access_key,
                    aws_secret_access_key=self.config.aws_secret_key,
                    region_name=self.region_name
                )
            except Exception as e:
                logger.error(f"Erro ao criar cliente S3: {e}")
                raise
        return self._s3_client
    
    def load(self, data: List[Dict[str, Any]], **kwargs) -> bool:
        """
        Carrega dados no S3, salvando-os como arquivo JSON.
        
        Args:
            data: Lista de registros a serem carregados
            **kwargs: Parâmetros adicionais (object_name, content_type, metadata)
            
        Returns:
            bool: True se o carregamento for bem-sucedido, False caso contrário
        """
        if not data:
            logger.warning("Nenhum dado para carregar no S3")
            return False
        
        if not self.validate_destination():
            logger.error("AWS S3 não está configurado corretamente")
            return False
        
        object_name = kwargs.get("object_name")
        content_type = kwargs.get("content_type", "application/json")
        metadata = kwargs.get("metadata", {})
        
        if not object_name:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_name = f"news_data_{timestamp}.json"
        
        try:
            with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
                json.dump(data, tmp, ensure_ascii=False, indent=4)
                tmp_filename = tmp.name
            
            extra_args = {
                "ContentType": content_type
            }
            
            if metadata:
                extra_args["Metadata"] = {
                    str(k): str(v) for k, v in metadata.items()
                }
            
            self.s3_client.upload_file(
                tmp_filename, 
                self.bucket_name, 
                object_name,
                ExtraArgs=extra_args
            )
            
            os.unlink(tmp_filename)
            
            logger.info(f"Carregados {len(data)} registros no S3: {self.bucket_name}/{object_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados no S3: {e}")
            
            if 'tmp_filename' in locals():
                try:
                    os.unlink(tmp_filename)
                except:
                    pass
                    
            return False
    
    def validate_destination(self) -> bool:
        """
        Valida se o bucket S3 existe e se temos acesso.
        
        Returns:
            bool: True se o bucket estiver acessível, False caso contrário
        """
        if not all([self.config.aws_access_key, self.config.aws_secret_key, self.bucket_name]):
            logger.error("Credenciais AWS ou nome do bucket não configurados")
            return False
            
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.error(f"O bucket '{self.bucket_name}' não existe")
            elif error_code == '403':
                logger.error(f"Sem permissão para acessar o bucket '{self.bucket_name}'")
            else:
                logger.error(f"Erro ao validar bucket S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro ao validar conexão com S3: {e}")
            return False
    
    def get_loader_name(self) -> str:
        """
        Retorna o nome do carregador.
        
        Returns:
            str: Nome do carregador
        """
        return "S3Uploader" 