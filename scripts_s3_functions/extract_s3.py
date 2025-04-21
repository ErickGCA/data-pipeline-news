import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    region_name=os.getenv("AWS_REGION")
)

response = s3.list_objects_v2(Bucket=os.getenv("S3_BUCKET_NAME"))

for obj in response.get('Contents', []):
    print(obj['Key'])
