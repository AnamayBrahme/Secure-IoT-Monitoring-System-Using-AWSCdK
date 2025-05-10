#!/usr/bin/env python3
import os

import aws_cdk as cdk

from drone_stack.drone_stack import DroneStack
from ProcessingStack.processing_stack import ProcessingStack
from AlertingStack.alertingstack import AlertingStack
from P4_MonitoringStack.p4_monitorinfstack import MonitoringStack

app = cdk.App()
DroneStack(app, "DroneStack")
ProcessingStack(app, "ProcessingStack")
AlertingStack(app,"AlertingStack")
monitoring_stack = MonitoringStack(
    app,
    "MonitoringStack",
    telemetry_lambda=ProcessingStack.telemetry_lambda,
    alert_lambda=AlertingStack.alert_lambda
)
app.synth()
