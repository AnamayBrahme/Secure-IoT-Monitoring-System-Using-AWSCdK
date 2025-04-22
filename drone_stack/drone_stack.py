from aws_cdk import (
    Duration,
    Stack,
    aws_sns as sns,
    aws_iot as iot,
    aws_iam as iam,
)
# This stack deploys the IOT Stack to receive messages from teh sensor

from constructs import Construct

class DroneStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Establishing the IoT Core
        drone_thing = iot.CfnThing(self, "DroneThing",thing_name="MySecureDrone")
        
        # Establishing the IOT Policy
        drone_policy = iot.CfnPolicy(self, "DronePolicy",policy_name="DroneIOTPolicy",
                                     policy_document={
                                         "Version": "2012-10-17",
                                         "Statement": [
                                             {
                                                 "Effect": "Allow",
                                                 "Action": ["iot:Publish",
                                                            "iot:Subscribe",
                                                            "iot:Receive",
                                                            "iot:Connect"
                                                            ],
                                                            "Resource": ["*"]
                                             }
                                        ]
                                     }
                                )
        # Establishing the IOT Certificate for  IOT Thing
        drone_cert = iot.CfnCertificate(self, "DroneCert", status="ACTIVE")

        # Attaching IOT Certificaate to Thing
        iot.CfnThingPrincipalAttachment(self, "AttachCertToThing",thing_name=drone_thing.thing_name,principal=drone_cert.attr_arn)

        # Attach Policy to Certificate
        iot.CfnPolicyPrincipalAttachment(self, "AttachPolicyToCert",policy_name=drone_policy.policy_name,principal=drone_cert.attr_arn)

        