# Extratores

Os extratores são responsáveis por coletar dados de diferentes fontes de notícias e retorná-los em um formato padronizado para processamento posterior.

## BaseExtractor

A interface base para todos os extratores implementa os seguintes métodos:

```python
@abstractmethod
def extract(self, query: str, from_date: str, to_date: str, **kwargs) -> List[Dict[str, Any]]:
    """Extrai dados da fonte"""
    
@abstractmethod
def validate_source(self) -> bool:
    """Valida a disponibilidade da fonte"""
    
@abstractmethod
def get_source_name(self) -> str:
    """Retorna o nome da fonte"""
```

## Implementações Disponíveis

### NewsAPIExtractor

Extrator para a API NewsAPI (https://newsapi.org/).

**Características:**
- Requer uma chave de API
- Suporta filtros por data, idioma e país
- Retorna artigos em formato JSON padronizado

**Exemplo de uso:**
```python
from src.etl.extractors.news_api_extractor import NewsAPIExtractor

extractor = NewsAPIExtractor()
articles = extractor.extract(
    query="acidente AND álcool",
    from_date="2023-01-01",
    to_date="2023-01-10",
    language="pt"
)
```

### GNewsExtractor

Extrator para a API GNews (https://gnews.io/).

**Características:**
- Requer uma chave de API
- Suporta filtros por data, idioma e país
- Retorna artigos em formato JSON padronizado

**Exemplo de uso:**
```python
from src.etl.extractors.gnews_extractor import GNewsExtractor

extractor = GNewsExtractor()
articles = extractor.extract(
    query="acidente AND álcool",
    from_date="2023-01-01",
    to_date="2023-01-10",
    language="pt",
    country="br"
)
```

## Criando um Novo Extrator

Para criar um novo extrator, basta implementar a interface `BaseExtractor`:

```python
from src.etl.extractors.base_extractor import BaseExtractor

class MyNewExtractor(BaseExtractor):
    def extract(self, query, from_date, to_date, **kwargs):
        # Implementação específica para obter dados da fonte
        # ...
        return articles
        
    def validate_source(self):
        # Verificar se a fonte está disponível
        # ...
        return True
        
    def get_source_name(self):
        return "MyNewsSource"
``` 