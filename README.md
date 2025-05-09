# News ETL Pipeline with SOLID Architecture

This project implements an ETL (Extract, Transform, Load) pipeline to process news related to car accidents involving alcohol consumption, following SOLID principles for improved maintainability and extensibility.

---

## Project Structure

The project follows a SOLID architecture with clear separation of responsibilities:

```
📁 pipelines-news/
├── 📁 src/                           # Source code with SOLID architecture
│   ├── 📁 etl/                       # Core ETL components
│   │   ├── 📁 extractors/            # Data extraction components
│   │   │   ├── 📄 base_extractor.py  # Interface for all extractors
│   │   │   ├── 📄 news_api_extractor.py # NewsAPI implementation
│   │   │   └── 📄 gnews_extractor.py # GNews API implementation
│   │   │
│   │   ├── 📁 transformers/          # Data transformation components
│   │   │   ├── 📄 base_transformer.py # Interface for all transformers
│   │   │   └── 📄 news_transformer.py # Filtering and relevance scoring
│   │   │
│   │   └── 📁 loaders/               # Data loading components
│   │       ├── 📄 base_loader.py     # Interface for all loaders
│   │       ├── 📄 postgres_loader.py # Loads data to PostgreSQL
│   │       └── 📄 s3_uploader.py     # Uploads data to Amazon S3
│   │
│   └── 📁 utils/                     # Shared utilities
│       ├── 📄 config.py              # Centralized configuration management
│       ├── 📄 logger.py              # Standardized logging system
│       └── 📄 database.py            # Database connection handling
│
├── 📁 docker/                        # Infrastructure configuration
│   ├── 📁 services/                  # Service-specific configurations
│   │   ├── 📁 airflow/               # Airflow configuration
│   │   │   ├── 📄 Dockerfile         # Custom Airflow image
│   │   │   └── 📄 requirements.txt   # Python dependencies
│   │   │
│   │   └── 📁 postgres/              # PostgreSQL configuration
│   │       └── 📁 init-scripts/      # Database initialization scripts
│   │           └── 📄 init-db.sql    # SQL setup script
│   │
│   ├── 📁 dags/                      # Airflow DAGs
│   │   └── 📁 pipelines/             # Pipeline definitions
│   │       ├── 📄 news_etl_dag.py    # New SOLID-based DAG implementation
│   │       └── 📄 etl_pipeline_dag.py # Legacy DAG (preserved for reference)
│   │
│   ├── 📁 data/                      # Data storage
│   │   ├── 📁 raw/                   # Raw extracted data
│   │   └── 📁 processed/             # Transformed data
│   │
│   ├── 📁 logs/                      # Airflow logs
│   ├── 📁 plugins/                   # Airflow plugins
│   ├── 📄 docker-compose.yml         # Docker services configuration
│   └── 📄 README.md                  # Docker setup documentation
│
├── 📄 README.md                      # Main project documentation
└── 📄 requirements.txt               # Python dependencies for local development
```

> **Note**: The legacy structure has been preserved for backward compatibility while transitioning to the new architecture.

---

## How to Run

### Local Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/ErickGCA/data-pipeline-news.git
   cd pipelines-news
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your `.env` file:
   ```ini
   AWS_ACCESS_KEY=...
   AWS_SECRET_KEY=...
   AWS_REGION=...
   S3_BUCKET=...
   NEWS_API_KEY=...
   GNEWS_API_KEY=...
   NEWSDATA_API_KEY=...
   POSTGRES_USER=...
   POSTGRES_PASSWORD=...
   POSTGRES_DB=...
   POSTGRES_PORT=...
   POSTGRES_HOST=...
   LOG_TO_FILE=True
   ```

---

### Environment with Docker and Airflow

1. Start Docker, then launch the containers:
   ```bash
   cd docker
   docker-compose up -d
   ```

2. Access Airflow via browser:
   [http://localhost:8080](http://localhost:8080)

3. In Airflow:
   - Find the `news_etl_pipeline` DAG (new SOLID architecture)
   - Enable and run the pipeline through the interface

---

## Architecture Benefits

The new SOLID architecture provides several advantages:

- **Single Responsibility**: Each component has one focused responsibility
- **Open/Closed**: New extractors, transformers, or loaders can be added without modifying existing code
- **Liskov Substitution**: Components are interchangeable as long as they follow the interfaces
- **Interface Segregation**: Clean interfaces for each component type
- **Dependency Inversion**: High-level modules depend on abstractions, not implementations

This makes the codebase more maintainable, testable, and extensible.

---

## Notes

- Ensure that the AWS credentials are correct to avoid errors when uploading to S3
- Make sure all API keys are correct
- Ensure PostgreSQL credentials are correct
- The project requires Docker with docker-compose for the full infrastructure
