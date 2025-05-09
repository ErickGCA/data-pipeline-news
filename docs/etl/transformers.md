# Transformadores

Os transformadores são responsáveis por processar, limpar e enriquecer os dados extraídos das fontes de notícias.

## BaseTransformer

A interface base para todos os transformadores implementa os seguintes métodos:

```python
@abstractmethod
def transform(self, data: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
    """Transforma os dados"""
    
@abstractmethod
def validate_transformation(self, data: List[Dict[str, Any]]) -> bool:
    """Valida os dados transformados"""
```

## Implementações Disponíveis

### NewsTransformer

Transformador específico para notícias relacionadas a acidentes com álcool.

**Características:**
- Normaliza formatos de data e hora
- Remove duplicatas baseadas em título ou conteúdo
- Padroniza campos e formatos
- Classifica notícias por relevância
- Extrai entidades e informações adicionais do texto

**Exemplo de uso:**
```python
from src.etl.transformers.news_transformer import NewsTransformer

transformer = NewsTransformer()
transformed_articles = transformer.transform(
    data=articles,
    deduplicate=True
)
```

**Pipeline de transformação:**

O `NewsTransformer` aplica as seguintes etapas de transformação:

1. **Normalização de Campos** - Padroniza nomes e formatos de campos
2. **Limpeza de Texto** - Remove HTML, caracteres especiais e formata o texto
3. **Detecção de Duplicatas** - Identifica e remove artigos duplicados
4. **Classificação** - Avalia relevância para o tema (acidentes com álcool)
5. **Enriquecimento** - Adiciona metadados e informações extraídas do texto

## Criando um Novo Transformador

Para criar um transformador personalizado, implemente a interface `BaseTransformer`:

```python
from src.etl.transformers.base_transformer import BaseTransformer

class MyCustomTransformer(BaseTransformer):
    def transform(self, data, **kwargs):
        # Implementação de transformação específica
        # ...
        return transformed_data
        
    def validate_transformation(self, data):
        # Código para validar os dados transformados
        # ...
        return True
``` 