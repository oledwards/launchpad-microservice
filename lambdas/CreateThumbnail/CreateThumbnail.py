import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import json
import time


s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)

def handler(event, context):
    for record in event['Records']:
        print("Context")
        print(context)
        payload = record["body"]
        sqs_message=json.loads(str(payload))
        bucket_name =  json.loads(str(sqs_message["Message"]))["Records"][0]["s3"]["bucket"]["name"]
        print(bucket_name)
        key=json.loads(str(sqs_message["Message"]))["Records"][0]["s3"]["object"]["key"]
        print(key)
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key.split("/")[1]) #working code
        upload_path = '/tmp/resized-{}'.format(key.split("/")[1])
        print(download_path)
        print(upload_path)
        s3_client.download_file(bucket_name, key, download_path)
        resize_image(download_path, upload_path)
        s3.meta.client.upload_file(upload_path, bucket_name, 'thumbnail/Thumbail-'+key.split("/")[1]) #creates folder within ingest bucket
        print("Successfully resized into thumbnail")