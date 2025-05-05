import boto3
import os
from datetime import datetime
import random
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def handler(event, context):
    print("Received event:", json.dumps(event))  # Log the received event
    device_id = event.get("deviceId", "unknown")
    timestamp = datetime.utcnow().isoformat()

    # Extract telemetry data with defaults
    battery = event.get("battery", round(random.uniform(10, 100), 2))  # Default to random battery level if not provided
    gyro = event.get("gyro", {"x","y","z",})  
    # Default to random gyro data if not provided
    temperature = event.get("temperature")

    # Store the item in DynamoDB
    table.put_item(Item={
        "drone_id": device_id,
        "timestamp": timestamp,
        "rawData": event,
        "battery": battery,
        "gyro": gyro,
        "temperature": temperature,
    })

    return {
        "statusCode": 200,
        "body": json.dumps("Stored successfully")
    }