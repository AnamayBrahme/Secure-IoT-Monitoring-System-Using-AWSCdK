import paho.mqtt.client as mqtt
import ssl
import time
import json
import random

# --- CONFIGURATION ---

MQTT_ENDPOINT = "localhost"  # or AWS IoT endpoint in prod
MQTT_PORT = 8883
THING_NAME = "MySecureDrone"
TOPIC = "drone/telemetry"

# Replace with paths to certs downloaded/generated from CDK/IoT
CA_CERT = "certs/AmazonRootCA1.pem"
CLIENT_CERT = "certs/device.pem.crt"
PRIVATE_KEY = "certs/private.pem.key"

# --- SIMULATION LOGIC ---

def generate_payload():
    return json.dumps({
        "drone_id": THING_NAME,
        "battery": round(random.uniform(10, 100), 2),
        "gyro": {
            "x": round(random.uniform(-1.0, 1.0), 2),
            "y": round(random.uniform(-1.0, 1.0), 2),
            "z": round(random.uniform(-1.0, 1.0), 2),
        },
        "temperature": round(random.uniform(30, 40), 2),
        "timestamp": int(time.time())
    })

def on_connect(client, userdata, flags, rc):
    print(f"[CONNECTED] with result code {rc}")
    if rc == 0:
        print("MQTT connection established.")
    else:
        print("MQTT connection failed.")

# --- MAIN ---

client = mqtt.Client(client_id=THING_NAME)
client.on_connect = on_connect

client.tls_set(ca_certs=CA_CERT,
               certfile=CLIENT_CERT,
               keyfile=PRIVATE_KEY,
               cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLS,
               ciphers=None)

print(f"Connecting to {MQTT_ENDPOINT}:{MQTT_PORT}...")
client.connect(MQTT_ENDPOINT, MQTT_PORT, 60)

client.loop_start()

try:
    while True:
        payload = generate_payload()
        print(f"[PUBLISH] {payload}")
        client.publish(TOPIC, payload)
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped by user.")
    client.loop_stop()
    client.disconnect()
