import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configurações
bucket_name = os.getenv("S3_BUCKET_NAME")
file_key = "filtered_news.json"
local_file_path = f"./{file_key}"

# Cliente S3
s3 = boto3.client(
    's3',
    region_name=os.getenv("AWS_REGION")
)

# Baixar arquivo
s3.download_file(bucket_name, file_key, local_file_path)
print(f"Arquivo baixado: {local_file_path}")

# Ver conteúdo
with open(local_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n🔍 Conteúdo do JSON:\n")
print(json.dumps(data, indent=2, ensure_ascii=False))
