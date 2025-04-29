import boto3
import os
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    print("Received event:", event)
    device_id = event.get("deviceId", "unknown")
    timestamp = datetime.utcnow().isoformat()

    table.put_item(Item={
        "deviceId": device_id,
        "timestamp": timestamp,
        "rawData": event
    })

    return {"statusCode": 200, "body": "Stored successfully"}
