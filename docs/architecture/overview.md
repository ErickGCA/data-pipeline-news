# Visão Geral da Arquitetura

O projeto segue uma arquitetura modular baseada nos princípios SOLID, facilitando a manutenção, testabilidade e extensibilidade.

## Estrutura do Projeto

```
src/
├── etl/
│   ├── extractors/       # Extratores de diferentes fontes de notícias
│   ├── transformers/     # Transformadores para processar notícias
│   └── loaders/          # Carregadores para diferentes destinos
├── utils/
│   ├── config.py         # Gerenciamento de configuração
│   ├── logger.py         # Sistema de logging centralizado
│   └── database.py       # Utilitário para conexão com banco de dados
└── __init__.py
```

## Fluxo de Dados

O fluxo de dados no pipeline segue estas etapas principais:

1. **Extração**: Coleta de notícias de múltiplas fontes (NewsAPI, GNews)
2. **Transformação**: Processamento e filtragem das notícias 
3. **Carregamento**: Armazenamento no PostgreSQL e Amazon S3

## Diagrama de Componentes

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Extratores │────>│Transformador│────>│ Carregadores│
│  (NewsAPI,  │     │    (News)   │     │ (PostgreSQL,│
│   GNews)    │     │             │     │     S3)     │
└─────────────┘     └─────────────┘     └─────────────┘
        │                  │                   │
        └──────────────────┼───────────────────┘
                           ▼
                    ┌─────────────┐
                    │  Utilitários│
                    │   (Config,  │
                    │    Logger)  │
                    └─────────────┘
```

## Orquestração

A orquestração do pipeline é realizada pelo Apache Airflow através de uma DAG (Directed Acyclic Graph) que coordena a execução das tarefas de extração, transformação e carregamento.

```
extract_news ──> transform_news ──┬──> load_to_postgres
                                  │
                                  └──> upload_to_s3
``` 