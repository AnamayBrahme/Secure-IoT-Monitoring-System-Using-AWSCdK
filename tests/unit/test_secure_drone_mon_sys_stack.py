import aws_cdk as core
import aws_cdk.assertions as assertions

from secure_drone_mon_sys.secure_drone_mon_sys_stack import SecureDroneMonSysStack

# example tests. To run these tests, uncomment this file along with the example
# resource in secure_drone_mon_sys/secure_drone_mon_sys_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SecureDroneMonSysStack(app, "secure-drone-mon-sys")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
