
# News ETL Pipeline

This project aims to build an ETL (Extract, Transform, Load) pipeline to process news related to car accidents involving the use of alcoholic beverages.

---

## Project Structure

- `docker/`
  - Contains configuration files to set up the environment with **Docker Compose**.
  - Spins up containers for:
    - **PostgreSQL** (database).
    - **Apache Airflow** (pipeline orchestration).
  
  - Subfolders:
    - `data/raw`
      - Stores locally extracted data that has not been processed yet.
    - `data/processed`
      - Stores locally transformed data.
    - `dags/pipelines`: DAGs used in Airflow with adapted ETL scripts.
    - `utils`: Modular extraction and deduplication scripts.
    - `logs/`: Directory for Airflow logs.
    - `plugins/`: Custom Airflow plugins (not in use currently).

- `scripts_s3_functions/`
  - Auxiliary scripts to work with visualization, extraction, and downloading from S3 (in development).

- `docker-compose.yml`
  - The main file to bring up all required containers.

- `requirements.txt`
  - List of Python dependencies needed to run the project locally.

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
   AWS_ACCESS_KEY_ID=...
   AWS_SECRET_ACCESS_KEY=...
   AWS_REGION=...
   S3_BUCKET_NAME=...
   NEWS_API_KEY=...
   AIRFLOW__CORE__SQL__ALCHEMY__CONN=...
   AIRFLOW__CORE__LOAD_EXAMPLES=...
   POSTGRES_USER=...
   POSTGRES_PASSWORD=...
   POSTGRES_DB=...
   POSTGRES_PORT=...
   POSTGRES_HOST=...
   ```

4. Run the ETL manually:
   ```bash
   python docker/dags/pipelines/main_etl.py
   ```

---

### Environment with Docker and Airflow

1. Open Docker, bring up the containers:
   ```bash
   cd docker
   docker compose up -d
   ```

2. Access Airflow via browser:

   [http://localhost:8080](http://localhost:8080)

3. In Airflow for manual activation:
   - Enable the `etl_pipeline_diario` DAG.
   - Run the pipeline through the interface.

---

## Notes

- Ensure that the AWS credentials are correct to avoid errors when uploading to S3.
- Make sure other API_KEYS are correct.
- Ensure PostgreSQL credentials are correct.
- Ensure Docker is running and that `requirements.txt` is installed.
