# Estrutura de Pipeline ETL

Este diretório contém a configuração do ambiente Docker para o pipeline ETL de notícias, agora seguindo princípios SOLID.

## Estrutura de Diretórios

```
docker/
├── docker-compose.yml      # Configuração dos serviços
├── .env.example            # Exemplo de variáveis de ambiente necessárias
├── data/                   # Diretório para armazenamento de dados
│   ├── raw/                # Dados brutos extraídos
│   └── processed/          # Dados processados
│
├── services/               # Configurações específicas de serviço
│   ├── airflow/            # Configurações do Airflow
│   │   ├── Dockerfile      # Imagem personalizada
│   │   └── requirements.txt # Dependências Python
│   └── postgres/           # Configurações do PostgreSQL
│       └── init-scripts/   # Scripts de inicialização
│           └── init-db.sql # Script de inicialização do banco
│
├── dags/                   # DAGs do Airflow
│   ├── pipelines/          # DAGs atuais
│   │   └── news_etl_dag.py # Nova DAG usando arquitetura SOLID
│   └── legacy/             # DAGs antigas mantidas para referência
│
├── logs/                   # Logs do Airflow
└── plugins/                # Plugins do Airflow
```

## Componentes Principais

O pipeline foi reorganizado seguindo princípios SOLID:

1. **Extratores**: Responsáveis por extrair dados de fontes de notícias (NewsAPI, GNews)
2. **Transformadores**: Processam e filtram notícias relacionadas a acidentes com álcool
3. **Carregadores**: Salvam os dados processados em diferentes destinos (PostgreSQL, S3)

## Como Usar

1. Configure as variáveis de ambiente:
   ```
   cp .env.example .env
   # Edite o arquivo .env com suas credenciais
   ```

2. Inicie os serviços:
   ```
   docker-compose up -d
   ```

3. Acesse a interface web do Airflow:
   ```
   http://localhost:8080
   ```

## Arquitetura SOLID

Esta nova estrutura segue os princípios SOLID:

- **S**: Cada componente tem uma única responsabilidade
- **O**: A arquitetura é extensível sem modificar código existente
- **L**: Os extratores/transformadores/carregadores são intercambiáveis
- **I**: Interfaces específicas para cada tipo de operação
- **D**: Componentes de alto nível não dependem de implementações de baixo nível

O código fonte da lógica ETL agora está na pasta `src/` na raiz do projeto. 