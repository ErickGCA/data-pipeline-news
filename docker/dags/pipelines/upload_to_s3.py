# upload_to_s3.py

import logging
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("upload_to_s3")

load_dotenv()


def upload_to_s3(file_path, bucket_name, object_name=None, content_type=None):
    if not os.path.exists(file_path):
        logger.error(f"Arquivo não encontrado: {file_path}")
        return False

    if object_name is None:
        object_name = os.path.basename(file_path)

    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        logger.error("Credenciais AWS não encontradas nas variáveis de ambiente")
        return False

    region_name = os.getenv("AWS_REGION", "us-east-1")
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=region_name,
        )
    except Exception as e:
        logger.error(f"Erro ao criar cliente S3: {e}")
        return False

    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type
    elif file_path.lower().endswith(".json"):
        extra_args["ContentType"] = "application/json"

    try:
        if extra_args:
            s3.upload_file(file_path, bucket_name, object_name, ExtraArgs=extra_args)
        else:
            s3.upload_file(file_path, bucket_name, object_name)

        logger.info(
            f"Arquivo '{file_path}' enviado com sucesso para '{bucket_name}/{object_name}'"
        )
        return True

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            logger.error(f"O bucket '{bucket_name}' não existe")
        elif e.response["Error"]["Code"] == "AccessDenied":
            logger.error(f"Acesso negado ao bucket '{bucket_name}'")
        else:
            logger.error(f"Erro no cliente S3: {e}")
        return False

    except FileNotFoundError:
        logger.error(f"Arquivo não encontrado: {file_path}")
        return False

    except Exception as e:
        logger.error(f"Erro inesperado ao enviar para o S3: {e}")
        return False


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "data" / "processed" / "processed_news.json"
    bucket_name = os.getenv("S3_BUCKET_NAME")
    object_name = "processed_news.json"

    if not bucket_name:
        logger.error("S3_BUCKET_NAME não definido nas variáveis de ambiente")
    else:
        success = upload_to_s3(str(file_path), bucket_name, object_name)
        if not success:
            logger.error("Upload para S3 falhou")
