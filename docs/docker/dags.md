# DAGs do Airflow

O projeto utiliza Apache Airflow para orquestrar os processos ETL. As DAGs (Directed Acyclic Graphs) definem o fluxo de trabalho e a sequência de tarefas a serem executadas.

## Estrutura de Diretórios

As DAGs estão localizadas no diretório `docker/dags/pipelines/`:

```
docker/
  └── dags/
      ├── pipelines/
      │   ├── news_etl_dag.py        # DAG principal refatorada com SOLID
      │   ├── etl_pipeline_dag.py    # DAG anterior
      │   ├── extract_news.py        # Módulo para extração
      │   ├── transform_news.py      # Módulo para transformação
      │   ├── load_to_postgres.py    # Módulo para carregamento no PostgreSQL
      │   ├── upload_to_s3.py        # Módulo para upload no S3
      │   └── main_etl.py            # Script ETL monolítico original
      └── utils/                     # Utilitários
```

## DAG Principal: news_etl_dag.py

A DAG principal do projeto foi refatorada para usar a nova arquitetura SOLID:

### Tarefas

1. **extract_news** - Extrai notícias de múltiplas fontes (NewsAPI, GNews)
2. **transform_news** - Transforma e filtra notícias para identificar as relevantes
3. **load_to_postgres** - Carrega notícias processadas no PostgreSQL
4. **upload_to_s3** - Carrega notícias processadas no Amazon S3

### Fluxo de Execução

```
extract_news ──> transform_news ──┬──> load_to_postgres
                                  │
                                  └──> upload_to_s3
```

### Programação

A DAG é executada diariamente às 8:00 (UTC):

```python
with DAG(
    dag_id="news_etl_pipeline",
    default_args=default_args,
    description="ETL Pipeline para extração e análise de notícias sobre acidentes com álcool",
    schedule_interval="0 8 * * *",  # Diariamente às 8:00
    start_date=days_ago(1),
    catchup=False,
    tags=["news", "etl", "solid"],
) as dag:
    # Definição das tarefas...
```

## Configuração

As configurações da DAG são gerenciadas pela classe `Config`:

```python
# Inicializar configuração
config = Config()

# Consulta para busca de notícias
NEWS_QUERY = '(acidente OR colisão OR batida OR capotamento OR atropelamento) AND (álcool OR alcoolizado OR embriaguez OR bêbado OR alcoolemia OR "lei seca")'
```

## Monitoramento

O Apache Airflow fornece uma interface web para monitorar a execução das DAGs:

1. Acesse http://localhost:8080
2. Faça login com as credenciais padrão (airflow/airflow)
3. Vá para DAGs > news_etl_pipeline

## Executando Manualmente

Para executar a DAG manualmente:

1. Na interface web do Airflow, encontre a DAG `news_etl_pipeline`
2. Clique no botão "Trigger DAG"
3. Opcional: defina parâmetros adicionais (ex: days_back=3)

Ou use a linha de comando:

```bash
docker-compose run airflow-cli airflow dags trigger news_etl_pipeline
``` 