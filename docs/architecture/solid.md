# Princípios SOLID no Projeto

Este projeto foi refatorado seguindo os princípios SOLID de design de software orientado a objetos, o que resulta em um código mais manutenível, extensível e testável.

## S - Princípio da Responsabilidade Única

Cada classe no projeto tem uma única responsabilidade:

- **Extratores**: Responsáveis apenas por extrair dados de uma fonte específica
- **Transformadores**: Responsáveis apenas por transformar e processar os dados
- **Carregadores**: Responsáveis apenas por carregar os dados em um destino específico
- **Config**: Responsável pelo gerenciamento de configurações
- **Logger**: Responsável pelo sistema de logging

## O - Princípio Aberto/Fechado

O projeto está aberto para extensão, mas fechado para modificação:

```python
# Nova fonte de notícias pode ser adicionada sem modificar o código existente
class CNNExtractor(BaseExtractor):
    def extract(self, query, from_date, to_date, **kwargs):
        # Implementação específica
        
    def validate_source(self):
        # Validação específica
        
    def get_source_name(self):
        return "CNN"
```

## L - Princípio da Substituição de Liskov

As implementações concretas podem ser substituídas pelas suas abstrações sem afetar o comportamento do programa:

```python
# Qualquer extrator pode ser usado aqui
def process_news(extractor: BaseExtractor, query, from_date, to_date):
    return extractor.extract(query, from_date, to_date)
    
# Funciona com qualquer implementação
news_api_articles = process_news(NewsAPIExtractor(), query, start_date, end_date)
gnews_articles = process_news(GNewsExtractor(), query, start_date, end_date)
```

## I - Princípio da Segregação de Interface

As interfaces são específicas para seus clientes, evitando métodos não utilizados:

- `BaseExtractor`: Interface específica para extratores
- `BaseTransformer`: Interface específica para transformadores
- `BaseLoader`: Interface específica para carregadores

## D - Princípio da Inversão de Dependência

O código depende de abstrações, não de implementações concretas:

```python
# A DAG depende das abstrações, não das implementações concretas
def extract_news(**kwargs):
    # NewsAPIExtractor e GNewsExtractor são inicializados aqui,
    # mas são usados através da interface BaseExtractor
    news_api_extractor = NewsAPIExtractor()
    gnews_extractor = GNewsExtractor()
    
    # Extrair usando as interfaces
    news_api_articles = news_api_extractor.extract(...)
    gnews_articles = gnews_extractor.extract(...)
```

## Benefícios da Arquitetura SOLID

1. **Manutenibilidade**: Fácil de entender e modificar
2. **Extensibilidade**: Fácil de adicionar novas funcionalidades
3. **Testabilidade**: Fácil de testar componentes isoladamente
4. **Reutilização**: Componentes podem ser reutilizados em outros contextos
5. **Flexibilidade**: Fácil de trocar implementações 