#!/usr/bin/env python3
import os

import aws_cdk as cdk

from drone_stack.drone_stack import DroneStack
from ProcessingStack.processing_stack import ProcessingStack
from AlertingStack.alertingstack import AlertingStack

app = cdk.App()
DroneStack(app, "DroneStack")
ProcessingStack(app, "ProcessingStack")
AlertingStack(app,"AlertingStack")
app.synth()
