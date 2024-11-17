import pandas as pd
import json
import boto3
import os

bucket = os.environ["bucket"]

def handler(event, ctx):
    if not event.get("body"):
        return response(400, "Bad Request")

    body = json.loads(event["body"])
    if not body.get("path"):
        return response(400, "Bad Request")

    path = body["path"]
    if path == "/upload":
        return handle_file_upload(body)
    elif path == "/predict":
        return handle_predict_data(body)

    return response(400, "Bad Request")

def response(code, body):
    return {
        "statusCode": code,
        "isBase64Encoded": False,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }

def handle_file_upload(body):
    if not body.get("raw_data") or not body.get("name"):
        return response(400, "Bad Request")

    name = body["name"]
    raw_data = body["raw_data"]

    client = boto3.client('s3')
    client.put_object(Body=raw_data.encode(), Bucket=bucket, Key=f"{name}.csv")

    return response(200, "Ok")

def handle_predict_data(body):
    if not body.get("volume") or not body.get("valve"):
        return response(400, "Bad Request")

    volume = int(body["volume"])
    valve = float(body["valve"])

    return response(200, "Ok")
