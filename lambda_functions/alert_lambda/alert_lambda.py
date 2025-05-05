import os
import json
import boto3

sns_client = boto3.client('sns')
TOPIC_ARN = os.environ['TOPIC_ARN']

# ===============================
# Modular Checks Matching Payload
# ===============================

def check_battery(data):
    battery = data.get('battery')
    if battery is not None and battery < 20:
        return f" Low battery warning: {battery}%"
    return None

def check_temperature(data):
    temp = data.get('temperature')
    if temp is not None and (temp > 38 or temp < 0):
        return f" Temperature abnormal: {temp}°C"
    return None

def check_gyro_stability(data):
    gyro = data.get('gyro', {})
    if not gyro:
        return " Missing gyro data"

    x, y, z = gyro.get('x'), gyro.get('y'), gyro.get('z')
    if any(abs(val) > 0.8 for val in (x, y, z)):
        return f" Drone stability issue - gyro readings too high: x={x}, y={y}, z={z}"
    return None

def check_missing_fields(data):
    required = ['battery', 'gyro', 'temperature', 'timestamp', 'drone_id']
    missing = [field for field in required if field not in data]
    if missing:
        return f" Missing telemetry fields: {', '.join(missing)}"
    return None

# ===============================
# Main Lambda Handler
# ===============================

def handler(event, context):
    print("Received event:", json.dumps(event))

    message = event.get('message')
    if not message and 'Records' in event:
        try:
            message = event['Records'][0]['Sns']['Message']
        except (KeyError, IndexError, TypeError):
            message = None

    if not message:
        print("No valid message found in event.")
        return {'statusCode': 400, 'alerts_sent': []}

    try:
        telemetry = json.loads(message) if isinstance(message, str) else message
    except json.JSONDecodeError:
        print("Failed to decode telemetry JSON.")
        return {'statusCode': 400, 'alerts_sent': []}

    print("Telemetry parsed:", telemetry)

    alerts = []
    for check in [check_battery, check_temperature, check_gyro_stability, check_missing_fields]:
        result = check(telemetry)
        if result:
            alerts.append(result)

    for alert in alerts:
        print(f"ALERT: {alert}")
        sns_client.publish(
            TopicArn=TOPIC_ARN,
            Message=alert,
            Subject="Drone Alert"
        )

    return {
        'statusCode': 200,
        'alerts_sent': alerts
    }
