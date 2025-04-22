from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_iam as iam,
    aws_iot as iot,
)
from constructs import Construct

class ProcessingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table for storing telemetry
        iot_table = ddb.Table(
            self, "TelemetryTable",
            partition_key=ddb.Attribute(name="deviceId", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="timestamp", type=ddb.AttributeType.STRING)
        )

        #Lambda Role with Inline Policy
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "DynamoAccessPolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "dynamodb:GetItem",
                                "dynamodb:PutItem",
                                "dynamodb:UpdateItem",
                                "dynamodb:Query",
                                "dynamodb:Scan",
                            ],
                            resources=[iot_table.table_arn]
                        ),
                        iam.PolicyStatement(
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                            ],
                            resources=["arn:aws:logs:*:*:*"]
                        )
                    ]
                )
            }
        )

        #  Lambda Function
        iot_lambda = _lambda.Function(
            self, "TelemetryDevice",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": iot_table.table_name
            },
            role=lambda_role
        )

        # IoT Rule Role with basic IoT permissions
        iot_rule_role = iam.Role(
            self,
            "IoTRuleExecutionRole",
            assumed_by=iam.ServicePrincipal("iot.amazonaws.com"),
            inline_policies={
                "IoTRulePolicy": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "iot:Publish",
                                "iot:Subscribe",
                                "iot:Unsubscribe",
                                "iot:Connect",
                                "lambda:InvokeFunction"
                            ],
                            resources=["*"]
                        )
                    ]
                )
            }
        )

        # IoT Topic Rule (connects MQTT topic to Lambda)
        topic_rule = iot.CfnTopicRule(
            self, "TelemetryRule",
            topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                sql="SELECT * FROM 'drone/telemetry'",
                actions=[
                    iot.CfnTopicRule.ActionProperty(
                        lambda_=iot.CfnTopicRule.LambdaActionProperty(
                            function_arn=iot_lambda.function_arn
                        )
                    )
                ],
                aws_iot_sql_version="2016-03-23",
                rule_disabled=False
            ),
            rule_name="TelemetryProcessingRule"
        )
