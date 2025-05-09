-- Criar esquema para dados de notícias
CREATE SCHEMA IF NOT EXISTS news_data;

-- Tabela para dados brutos de notícias
CREATE TABLE IF NOT EXISTS news_data.raw_news (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    content TEXT,
    url TEXT UNIQUE,
    publishedAt TIMESTAMP,
    source_name TEXT,
    source_id TEXT,
    original_source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para notícias processadas
CREATE TABLE IF NOT EXISTS news_data.processed_news (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    url TEXT UNIQUE,
    publishedAt TIMESTAMP,
    relevance_score INTEGER,
    source TEXT,
    original_source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para otimização de consultas
CREATE INDEX IF NOT EXISTS idx_raw_news_publishedat ON news_data.raw_news(publishedAt);
CREATE INDEX IF NOT EXISTS idx_processed_news_relevance ON news_data.processed_news(relevance_score);

-- Conceder permissões ao usuário do Airflow
GRANT ALL PRIVILEGES ON SCHEMA news_data TO airflow;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA news_data TO airflow;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA news_data TO airflow; 