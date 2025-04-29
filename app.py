#!/usr/bin/env python3
import os

import aws_cdk as cdk

from drone_stack.drone_stack import DroneStack
from ProcessingStack.processing_stack import ProcessingStack

app = cdk.App()
DroneStack(app, "DroneStack")
ProcessingStack(app, "ProcessingStack")
app.synth()
