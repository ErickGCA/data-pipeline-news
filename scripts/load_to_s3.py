import boto3
import os
from dotenv import load_dotenv

load_dotenv()


print(os.getenv("AWS_ACCESS_KEY_ID"))
print(os.getenv("AWS_SECRET_ACCESS_KEY"))
print(os.getenv("S3_BUCKET_NAME"))


def upload_to_s3(file_path, bucket_name, object_name):
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),

        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"Arquivo '{file_path}' enviado com sucesso para '{bucket_name}/{object_name}'")
    except Exception as e:
        print(f"Erro ao enviar para o S3: {e}")

if __name__ == "__main__":
    file_path = "../data-pipeline-news/data/filtered_news.json"
    bucket_name = os.getenv("S3_BUCKET_NAME")
    object_name = "filtered_news.json"

    upload_to_s3(file_path, bucket_name, object_name)
