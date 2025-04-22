# Secure IoT Monitoring System 🚁🔒

This project is a simulation of a secure IoT-based telemetry and alerting system using AWS services.

## ✅ Phase 1: DroneStack (Complete ✅)
This phase provisions secure IoT device connectivity:
- IoT Thing, IoT Core
- MQTT topic for telemetry (`drone/telemetry`)
- IAM Role for IoT Thing
- X.509 Certificate (attached to the Thing)
- Local MQTT simulator using Python + `paho-mqtt`

💡 This sets up the foundation for device-to-cloud communication with strong identity and message routing.

## 📦 Phase 2: ProcessingStack (Completed ✅)

### Components:
- AWS IoT Rule
- AWS Lambda Function
- DynamoDB Table
- IAM Roles (with inline policies for secure access)

### Purpose:
Process telemetry data sent by the drone. An IoT Rule captures MQTT messages from the Phase 1 topic and triggers a Lambda function to store the data into DynamoDB.

---

## 🚀 Next Phase: Phase 3 (Coming Soon)

### AlertingStack
**Goal**: Add fault detection & notifications using:
- CloudWatch Metrics/Alarms
- Amazon SNS


## 💻 Simulator
Simulates telemetry messages using MQTT:

```bash
cd simulator
python mqtt_drone.py
