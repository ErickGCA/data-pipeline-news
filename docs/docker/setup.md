# Configuração Docker

O projeto utiliza Docker e Docker Compose para criar um ambiente de desenvolvimento completo com Apache Airflow, PostgreSQL e outros serviços necessários.

## Pré-requisitos

- Docker
- Docker Compose

## Arquivos de Configuração

O ambiente é definido pelo arquivo `docker-compose.yml` localizado na pasta `docker/`.

## Serviços

O Docker Compose configura os seguintes serviços:

- **PostgreSQL**: Banco de dados para armazenamento de notícias processadas
- **Airflow Webserver**: Interface web para gerenciamento do Airflow
- **Airflow Scheduler**: Programador de tarefas do Airflow
- **Airflow Worker**: Executor de tarefas do Airflow
- **Airflow Init**: Inicialização do Airflow
- **Airflow CLI**: Interface de linha de comando para o Airflow

## Volumes

Os seguintes volumes são configurados:

- **./dags**: Diretório para armazenar as DAGs do Airflow
- **./logs**: Logs do Airflow
- **./plugins**: Plugins do Airflow
- **./data**: Dados persistentes

## Iniciando o Ambiente

Para iniciar todos os serviços:

```bash
cd docker
docker-compose up -d
```

Para verificar o status dos contêineres:

```bash
docker-compose ps
```

Para parar todos os serviços:

```bash
docker-compose down
```

## Acesso aos Serviços

- **Airflow Web UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432

## Customização

Para personalizar o ambiente, você pode editar as seguintes variáveis no arquivo `docker-compose.yml`:

- **AIRFLOW__CORE__EXECUTOR**: Tipo de executor do Airflow
- **AIRFLOW__DATABASE__SQL_ALCHEMY_CONN**: String de conexão com o banco de dados do Airflow
- **POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB**: Credenciais do PostgreSQL 