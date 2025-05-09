import os
from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Dict, Optional, List
from .setup_all_directories import setup_all_directories

logger = logging.getLogger(__name__)

class DataLakeConfig:
    """
    Configuração e gerenciamento do Data Lake.
    Implementa uma estrutura de zonas: raw, processed, curated
    Cada zona tem suas próprias regras de retenção e metadados.
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        # Usa setup_all_directories para criar a estrutura base
        directories = setup_all_directories(base_dir)
        
        self.zones = {
            "raw": {
                "path": directories["raw_data_dir"],
                "retention_days": 30,
                "format": "json"
            },
            "processed": {
                "path": directories["processed_data_dir"],
                "retention_days": 90,
                "format": "json"
            },
            "curated": {
                "path": directories["curated_data_dir"],
                "retention_days": 365,
                "format": "parquet"
            }
        }
        
        # Cria diretório de metadados para cada zona
        for zone in self.zones.values():
            os.makedirs(os.path.join(zone["path"], "_metadata"), exist_ok=True)
            logger.info(f"Diretório de metadados criado/verificado: {zone['path']}/_metadata")
    
    def save_with_metadata(self, data: dict, zone: str, filename: str, metadata: Optional[dict] = None) -> tuple[str, str]:
        """
        Salva dados com metadados associados.
        
        Args:
            data: Dados a serem salvos
            zone: Zona do data lake (raw, processed, curated)
            filename: Nome do arquivo
            metadata: Metadados adicionais (opcional)
            
        Returns:
            Tuple com os caminhos dos arquivos de dados e metadados
        """
        if not metadata:
            metadata = {}
            
        # Adiciona metadados padrão
        metadata.update({
            "created_at": datetime.now().isoformat(),
            "zone": zone,
            "format": self.zones[zone]["format"],
            "filename": filename
        })
        
        # Salva os dados
        data_path = os.path.join(self.zones[zone]["path"], filename)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        # Salva os metadados
        metadata_filename = f"{os.path.splitext(filename)[0]}_metadata.json"
        metadata_path = os.path.join(self.zones[zone]["path"], "_metadata", metadata_filename)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
            
        logger.info(f"Dados e metadados salvos em {zone}: {filename}")
        return data_path, metadata_path
    
    def get_metadata(self, zone: str, filename: str) -> Optional[dict]:
        """
        Recupera os metadados de um arquivo.
        
        Args:
            zone: Zona do data lake
            filename: Nome do arquivo
            
        Returns:
            Dicionário com os metadados ou None se não encontrado
        """
        metadata_filename = f"{os.path.splitext(filename)[0]}_metadata.json"
        metadata_path = os.path.join(self.zones[zone]["path"], "_metadata", metadata_filename)
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def list_files(self, zone: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[str]:
        """
        Lista arquivos em uma zona com filtro opcional por data.
        
        Args:
            zone: Zona do data lake
            start_date: Data inicial para filtro (opcional)
            end_date: Data final para filtro (opcional)
            
        Returns:
            Lista de nomes de arquivos
        """
        path = self.zones[zone]["path"]
        if not os.path.exists(path):
            return []
            
        files = [f for f in os.listdir(path) if not f.startswith('_') and f.endswith('.json')]
        
        if start_date or end_date:
            filtered_files = []
            for file in files:
                try:
                    date_str = file.split('_')[2]  # Pega a parte da data
                    file_date = datetime.strptime(date_str, '%Y%m%d')
                    
                    if start_date and file_date < start_date:
                        continue
                    if end_date and file_date > end_date:
                        continue
                        
                    filtered_files.append(file)
                except (IndexError, ValueError):
                    continue
            return filtered_files
            
        return files

def get_data_lake_paths(base_dir: Optional[str] = None) -> Dict[str, Path]:
    """
    Retorna os caminhos do data lake.
    
    Args:
        base_dir: Diretório base do projeto. Se None, usa o diretório atual.
        
    Returns:
        Dicionário com os caminhos do data lake
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    data_dir = Path(base_dir) / "data"
    
    return {
        "raw": data_dir / "raw",
        "processed": data_dir / "processed",
        "curated": data_dir / "curated",
        "mock_data": data_dir / "mock_data"
    } 