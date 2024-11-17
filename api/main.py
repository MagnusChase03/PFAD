import pandas as pd
from sklearn.cluster import KMeans

from io import StringIO
import json
import boto3
import math
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

def handle_file_upload(body):
    if not body.get("raw_data") or not body.get("name"):
        return response(400, "Bad Request")

    name = body["name"]
    raw_data = body["raw_data"]

    client = boto3.client('s3')
    client.put_object(Body=raw_data.encode(), Bucket=bucket, Key=f"{name}.csv")

    df = pd.read_csv(StringIO(raw_data))
    center_x, center_y, threshold, error_threshold = preform_kmeans(df)

    cached_data = {
        "center_x": center_x,
        "center_y": center_y,
        "threshold": threshold,
        "error_threshold": error_threshold
    }
    client.put_object(Body=json.dumps(cached_data).encode(), Bucket=bucket, Key=f"{name}_cache.csv")

    return response(200, "Ok")

def preform_kmeans(df):
    old_setpoint = df.iloc[0, 2]
    old_percent_open = df.iloc[0, 3]
    for i in range(0, df.shape[0]):
        current_setpoint = df.iloc[i, 2]
        current_percent_open = df.iloc[i, 3]
        if math.isnan(df.iloc[i, 1]):
            df.iloc[i, 1] = 0.0
        if math.isnan(current_setpoint):
            df.iloc[i, 2] = old_setpoint
        if math.isnan(current_percent_open):
            df.iloc[i, 3] = old_percent_open
        old_setpoint = df.iloc[i, 2]
        old_percent_open = df.iloc[i, 3]

    dataset = []
    X = [] # Current volume
    y = [] # Valve open
    for i in range(0, df.shape[0]):
        X.append(df.iloc[i, 1])
        y.append(df.iloc[i, 3])
        dataset.append([df.iloc[i, 1], df.iloc[i, 3]])

    kmeans = kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(dataset)
    center_x = kmeans.cluster_centers_[0][0]
    center_y = kmeans.cluster_centers_[0][1]

    threshold = 100000
    total = 0
    count = 0
    for i in range(0, len(X)):
        point = [X[i].item(), y[i].item()]
        pred = kmeans.predict([point]).item()
        distance = math.sqrt((point[0] - center_x) ** 2 + (point[1] - center_y) ** 2)
        if pred == 0 and distance < threshold:
            total += distance
            count += 1
    threshold = total / count
    error_threshold = 4 * threshold

    return (center_x, center_y, threshold, error_threshold)

def handle_predict_data(body):
    if not body.get("volume") or not body.get("valve"):
        return response(400, "Bad Request")

    volume = int(body["volume"])
    valve = float(body["valve"])

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
