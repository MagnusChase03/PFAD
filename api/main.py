from io import StringIO
import base64
import json
import boto3
import math
import os

bucket = os.environ["bucket"]

def handler(event, ctx):
    req = event.get("requestContext")
    if req is None:
        return response(400, "Bad Request")

    http = req.get("http")
    if http is None:
        return response(400, "Bad Request")

    method = http.get("method")
    if not method == "POST":
        return response(400, "Bad Request")

    body = event.get("body")
    if body is None:
        return response(400, "Bad Request")

    handler = "request"
    try:
        body = json.loads(body)
    except Exception:
        handler = "file"
        body = base64.b64decode(body).decode()

    if handler == "request":
        return handle_request(body)
    else:
        return handle_file(body)

def handle_request(body):
    data = read_s3(body["filename"])
    return response(200, data)

def handle_file(body):
    start_i = body.find("filename=\"")
    end_i = start_i
    while body[end_i] != '\n':
        end_i += 1

    title = body[start_i:end_i]
    title = title[title.find("\"")+1:-2]

    body = "\n".join(body.split("\n")[4:])
    write_s3(title, body)

    dates, points = get_points(body)
    clusters, threshold, error_threshold, blockages = find_blockage(points)

    result_blockages = []
    result_volume = []
    result_valve = []
    for i in range(0, len(dates)):
        result_blockages.append({
            "Date": dates[i],
            "Blockage": blockages[i]
        })
        result_volume.append({
            "Date": dates[i],
            "Volume": points[i][0]
        })
        result_valve.append({
            "Date": dates[i],
            "Valve": points[i][1]
        })

    write_s3(title.split(".csv")[0] + "_results.csv", json.dumps({
        "clusters": clusters,
        "threshold": threshold,
        "error_threshold": error_threshold,
        "blockages": result_blockages,
        "volumes": result_volume,
        "valves": result_valve
    }))

    return response(200, "Ok")

def read_s3(filename):
    client = boto3.client('s3')
    req = client.get_object(Bucket=bucket, Key=filename)
    return req.Body.read().decode()

def write_s3(filename, data):
    client = boto3.client('s3')
    client.put_object(Bucket=bucket, Key=filename, Body=data.encode())

def get_points(csv_body):
    lines = csv_body.split("\n")
    lines = lines[1:]

    dates = []
    points = []
    old_valve = -1.0
    old_volume = -1.0
    for line in lines:
        fields = line.split(",")
        dates.append(fields[0])

        try:
            volume = float(fields[1])
        except:
            volume = old_volume

        try:
            valve = float(fields[3])
        except:
            valve = old_valve

        points.append([volume, valve])

        old_volume = old_volume
        old_valve = valve

    return (dates, points)

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

    return (clusters, threshold, error_threshold, blockages)

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
