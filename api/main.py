import pandas as pd
import json
import boto3
import os

def handler(event, ctx):
    bucket = os.environ["bucket"]
    if not event.get("body"):
        return response(400, "Bad Request")

    body = json.loads(event["body"])
    if not body.get("raw_data") or not body.get("name"):
        return response(400, "Bad Request")

    name = body["name"]
    raw_data = body["raw_data"]

    client = boto3.client('s3')
    client.put_object(Body=raw_data.encode(), Bucket=bucket, Key=f"{name}.csv")

    return response(200, "Ok")

def response(code, body):
    return {
        "statusCode": code,
        "isBase64Encoded": False,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }
