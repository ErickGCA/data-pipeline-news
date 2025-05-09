# Carregadores

Os carregadores são responsáveis por armazenar os dados processados em diferentes destinos como bancos de dados, serviços de armazenamento em nuvem ou arquivos locais.

## BaseLoader

A interface base para todos os carregadores implementa os seguintes métodos:

```python
@abstractmethod
def load(self, data: List[Dict[str, Any]], **kwargs) -> bool:
    """Carrega os dados no destino"""
    
@abstractmethod
def validate_destination(self) -> bool:
    """Valida se o destino está disponível"""
```

## Implementações Disponíveis

### PostgresLoader

Carregador para armazenamento em banco de dados PostgreSQL.

**Características:**
- Criar automaticamente tabelas se não existirem
- Suporta diferentes modos de inserção (append, replace, fail)
- Gerencia conexões e transações
- Otimizado para inserções em lote

**Exemplo de uso:**
```python
from src.etl.loaders.postgres_loader import PostgresLoader

loader = PostgresLoader()
success = loader.load(
    data=transformed_articles,
    table_name="news_data.processed_news",
    if_exists="append"
)
```

### S3Uploader

Carregador para armazenamento no Amazon S3.

**Características:**
- Upload de dados como arquivos JSON ou CSV
- Suporte para metadados e tags
- Controle de acesso e criptografia
- Versionamento automático

**Exemplo de uso:**
```python
from src.etl.loaders.s3_uploader import S3Uploader

uploader = S3Uploader()
success = uploader.load(
    data=transformed_articles,
    object_name="news/processed_news_2023-01-01.json",
    metadata={"source": "news_pipeline", "date": "2023-01-01"}
)
```

## Criando um Novo Carregador

Para criar um carregador personalizado, implemente a interface `BaseLoader`:

```python
from src.etl.loaders.base_loader import BaseLoader

class MySQLLoader(BaseLoader):
    def load(self, data, **kwargs):
        # Código para carregar dados no MySQL
        # ...
        return True
        
    def validate_destination(self):
        # Verificar conexão com MySQL
        # ...
        return True
``` 