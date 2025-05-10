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
## 📦 Phase 3: AlertingStack (Completed ✅)

### Components:
- AWS IoT Rule
- AWS Lambda Function - (alert_lambda.py)
- AWS SNS

### Purpose:
Implement an basic alerting system that triggers notifications when certain conditions are met (e.g., low battery, temperature abnormality).

## 📦 Phase 4: MonitoringStack (Completed ✅)

### Components:
- AWS CloudWatch  
- AWS Logs
- CloudWatch Metrics from Lambda & DynamoDB

### Purpose:
Provide a basic monitoring and observability layer for the IoT system. Visualizes system health using a CloudWatch Dashboard and leverages default service-level metrics.

## 🚀 Next Phase: Phase5 - APIGatewayStack  (Coming Soon)

### 
**Goal**: Enable on-demand data access for clients or dashboards through secure REST APIs. This will allow querying telemetry data (e.g., latest battery level, temperature) stored in DynamoDB, using HTTP endpoints exposed by API Gateway.

## 💻 Simulator
Simulates telemetry messages using MQTT:

```bash
cd simulator
python mqtt_drone.py
