from aws_cdk import (
    Stack,
    aws_cloudwatch as cw,
    Duration,
    aws_logs as logs, # if needed for dashboards
)
from constructs import Construct

class MonitoringStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,
                 telemetry_lambda, alert_lambda, table,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        battery_metric = cw.Metric(
            namespace="DroneTelemetry",
            metric_name="battery",
            statistic="Average",
            period=Duration.minutes(1)
        )

        temperature_metric = cw.Metric(
            namespace="DroneTelemetry",
            metric_name="temperature",
            statistic="Average",
            period=Duration.minutes(1)
        )

        # 🔹 LAMBDA: Invocation and Error Metrics
        telemetry_invokes = telemetry_lambda.metric_invocations()
        telemetry_errors = telemetry_lambda.metric_errors()

        alert_invokes = alert_lambda.metric_invocations()
        alert_errors = alert_lambda.metric_errors()

        # 🔹 DYNAMODB: Read/Write capacity metrics
        dynamo_reads = table.metric("ConsumedReadCapacityUnits")
        dynamo_writes = table.metric("ConsumedWriteCapacityUnits")

        # 🔹 DASHBOARD
        dashboard = cw.Dashboard(self, "DroneMonitoringDashboard")

        dashboard.add_widgets(
            cw.GraphWidget(
                title="Battery Levels",
                left=[battery_metric]
            ),
            cw.GraphWidget(
                title="Temperature",
                left=[temperature_metric]
            ),
            cw.GraphWidget(
                title="Telemetry Lambda Invocations",
                left=[telemetry_invokes, telemetry_errors]
            ),
            cw.GraphWidget(
                title="Alert Lambda Invocations",
                left=[alert_invokes, alert_errors]
            ),
            cw.GraphWidget(
                title="DynamoDB Activity",
                left=[dynamo_reads, dynamo_writes]
            )
        )