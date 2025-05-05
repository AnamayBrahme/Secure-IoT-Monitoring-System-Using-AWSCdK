from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_iot as iot
)
from constructs import Construct

class AlertingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        

        # 1. Define the SNS topic
        alert_topic = sns.Topic(self, "DroneAlertTopic", display_name="Drone Alerts Topic")

        # 2. Define the Lambda execution role
        alert_lambda_role = iam.Role(
            self, "AlertLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="IAM role for Alert Lambda with restricted permissions"
        )
        alert_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        alert_lambda_role.add_to_policy(
            iam.PolicyStatement(
                actions=["sns:Publish"],
                resources=[alert_topic.topic_arn]
            )
        )

        # 3. Define the Lambda function
        alert_lambda = _lambda.Function(
            self, "DroneAlertLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="alert_lambda.handler",
            code=_lambda.Code.from_asset("lambda_functions/alert_lambda"),
            environment={
                "TOPIC_ARN": alert_topic.topic_arn
            },
            role=alert_lambda_role
        )

        # 4. Allow IoT to invoke this Lambda
        alert_lambda.add_permission(
            "AllowIoTInvoke",
            principal=iam.ServicePrincipal("iot.amazonaws.com"),
            action="lambda:InvokeFunction"
        )

        # 6. IoT Topic Rule
        iot.CfnTopicRule(
            self, "AlertingTelemetryRule",
            topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                sql="SELECT * FROM 'drone/telemetry'",
                actions=[
                    iot.CfnTopicRule.ActionProperty(
                        lambda_=iot.CfnTopicRule.LambdaActionProperty(
                            function_arn=alert_lambda.function_arn
                        )
                    )
                ],
                aws_iot_sql_version="2016-03-23",
                rule_disabled=False
            ),
            rule_name="AlertingTelemetryRule"
        )

        