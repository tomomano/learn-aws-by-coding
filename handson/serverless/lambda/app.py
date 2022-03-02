from aws_cdk import (
    core,
    aws_lambda as _lambda
)
import os

# <1>
FUNC = """
import time
from random import choice, randint
def handler(event, context):
    time.sleep(randint(2,5))
    sushi = ["salmon", "tuna", "squid"]
    message = "Welcome to Cloud Sushi. Your order is " + choice(sushi)
    print(message)
    return message
"""

class SimpleLambda(core.Stack):

    def __init__(self, scope: core.App, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # <2>
        handler = _lambda.Function(
            self, 'LambdaHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.handler",
            code=_lambda.Code.from_inline(FUNC),
            memory_size=128,
            timeout=core.Duration.seconds(10),
            dead_letter_queue_enabled=True,
        )

        core.CfnOutput(self, "FunctionName", value=handler.function_name)

app = core.App()
SimpleLambda(
    app, "SimpleLambda",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)
app.synth()
