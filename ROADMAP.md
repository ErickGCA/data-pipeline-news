# 📈 Roadmap - Projeto de Pipeline de Dados de Notícias

---

## ✅ Etapa 1: ETL Manual e Simples
- [x] Coletar dados de uma API de notícias (NewsAPI).
- [x] Filtrar notícias relacionadas a acidentes de carro com álcool.
- [x] Salvar os dados localmente (`.json` ou `.csv`).
- [x] Fazer upload dos arquivos para o Amazon S3 usando `boto3`.

---

## ✅ Etapa 2: Automação com Python Puro
- [x] Criar `main_etl.py` para orquestrar o processo de ETL completo.
- [x] Automatizar a execução manual do ETL.
- [x] **(AWS Lambda foi deixado de lado para focar no ambiente local e facilitar o uso do projeto via GitHub).**

---

## ✅ Etapa 3: Orquestração com Apache Airflow
- [x] Subir PostgreSQL e Apache Airflow localmente com Docker Compose.
- [x] Configurar Airflow com conexão no PostgreSQL.
- [x] Criar DAG no Airflow para orquestrar o ETL.
- [x] Rodar e monitorar o pipeline via interface web do Airflow.

---

## ✅ Etapa 4: Validação e Qualidade dos Dados
- [x] Adicionar validações nos dados:
  - Conferir se as colunas esperadas estão presentes.
  - Tratar valores nulos ou inconsistências.
- [x] Criar logs ou relatórios simples de erros detectados.
- [x] Adicionar novas API's de notícias (GNews, NewsData).

---

## ✅ Etapa 5: Refatoração para Arquitetura SOLID
- [x] Implementar interfaces base (BaseExtractor, BaseTransformer, BaseLoader).
- [x] Aplicar princípio da Responsabilidade Única separando extratores, transformadores e carregadores.
- [x] Melhorar gerenciamento de configuração com padrão Singleton.
- [x] Padronizar o sistema de logging em toda a aplicação.
- [x] Criar estrutura modular para facilitar extensões futuras.
- [x] Refatorar Docker e Airflow para trabalhar com a nova arquitetura.

---

## 🧊 Etapa 6: Armazenamento Estruturado
- [x] Criar tabelas e schemas apropriados para consultas SQL no PostgreSQL.
- [ ] Integrar o pipeline com Amazon Redshift, Athena ou Snowflake.
- [ ] Implementar sistema de migração de esquema (usando Alembic ou similar).

---

## 🧪 Etapa 7: Testes Automatizados
- [ ] Implementar testes unitários para todos os componentes.
- [ ] Configurar testes de integração para o pipeline completo.
- [ ] Adicionar verificações de cobertura de código.
- [ ] Configurar CI/CD para execução automática de testes.

---

## 📊 Etapa 8: Visualização
- [x] Conectar os dados no S3 ou banco de dados no Metabase, Superset ou Power BI.
- [ ] Criar dashboards de análise:
  - Número de acidentes por estado.
  - Número de acidentes por data.
  - Outros insights relevantes.
- [ ] Desenvolver API REST para acesso aos dados processados.

---

## 📦 Etapa 9: Empacotamento e Distribuição
- [ ] Configurar setup.py para transformar o projeto em pacote Python.
- [ ] Publicar pacote no PyPI para instalação via pip.
- [ ] Criar imagens Docker pré-configuradas para facilitar implantação.
- [x] Adicionar documentação automática com Sphinx ou MkDocs.

---

## 🧵 Etapa 10: Streaming de Dados (Extra/Opcional)
- [ ] Integrar Kafka ou Kinesis para ingestão contínua de notícias em tempo real.
- [ ] Adaptar o ETL para consumir e processar dados em streaming.
- [ ] Implementar análise em tempo real com Spark Streaming ou Flink.

---

# 🎯 Observação
O projeto foi desenhado para ser totalmente funcional com simples `git clone`, `docker compose up`, e execução do Airflow localmente, sem necessidade de configuração externa (ex: AWS Lambda, IAM roles).

A arquitetura SOLID implementada facilita a manutenção, testabilidade e extensibilidade do código, permitindo adicionar novas fontes de dados ou destinos com o mínimo de alterações no código existente.

