from io import StringIO
import json
import boto3
import math
import csv
import os

bucket = os.environ["bucket"]

def handler(event, ctx):
    return response(400, "Bad Request")

def find_blockage(data):
    clusters = kmeans(data, 2)

    total = 0
    count = 0
    for i in range(0, len(data)):
        d1 = distance(data[i][0], clusters[0][0], data[i][1], clusters[0][1])
        d2 = distance(data[i][0], clusters[1][0], data[i][1], clusters[1][1])
        if d1 < d2:
            total += d1
            count += 1
    threshold = 2 * total / count
    error_threshold = 4 * threshold

    blockages = []
    for i in range(0, len(data)):
        if data[i][0] < clusters[0][0] - error_threshold or data[i][1] > clusters[0][1] + error_threshold:
            blockages.append(2.0)
        elif data[i][0] < clusters[0][0] - threshold or data[i][1] > clusters[0][1] + threshold:
            blockages.append(1.0)
        else:
            blockages.append(0.0)

    return (threshold, error_threshold, blockages)

def kmeans(data, clusters):
    cluster = [data[i] for i in range(0, clusters)]
    for i in range(0, 100):
        totals = [[0.0, 0.0] for i in range(0, clusters)]
        counts = [0.0 for i in range(0, clusters)]
        for point in data:
            distances = []
            for c in range(0, len(cluster)):
                distances.append(distance(point[0], cluster[c][0], point[1], cluster[c][1]))
            min_i = min(distances)
            totals[min_i][0] += point[0]
            totals[min_i][1] += point[1]
            counts[min_i] += 1
        for c in range(0, len(clusters)):
            totals[c][0] = totals[c][0] / counts[c]
            totals[c][1] = totals[c][1] / counts[c]
            cluster[c] = totals[c]
    return cluster

def distance(x, x2, y, y2):
    return math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)

def min(distances):
    min_i = 0
    min = distances[0]
    for i in range(1, min_i):
        if distances[i] < min:
            min = distances[i]
            min_i = i
    return min_i

def response(code, body):
    return {
        "statusCode": code,
        "isBase64Encoded": False,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json"
        }
    }
