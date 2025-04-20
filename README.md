# Secure IoT Monitoring System 🚁🔒

This project is a simulation of a secure IoT-based telemetry and alerting system using AWS services.

## ✅ Phase 1: DroneStack (Complete)
This phase provisions secure IoT device connectivity:
- IoT Thing, IoT Core
- MQTT topic for telemetry (`drone/telemetry`)
- IAM Role for IoT Thing
- X.509 Certificate (attached to the Thing)
- Local MQTT simulator using Python + `paho-mqtt`

💡 This sets up the foundation for device-to-cloud communication with strong identity and message routing.

## 🔜 Phase 2: ProcessingStack (Coming Soon)
We will:
- Subscribe to telemetry with an **IoT Rule**
- Trigger a **Lambda function**
- Store telemetry data in **DynamoDB**

## 💻 Simulator
Simulates telemetry messages using MQTT:

```bash
cd simulator
python mqtt_drone.py
