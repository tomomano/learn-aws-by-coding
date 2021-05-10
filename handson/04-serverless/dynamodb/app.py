from aws_cdk import (
    core,
    aws_dynamodb as ddb
)
import os

class SimpleDynamoDb(core.Stack):

    def __init__(self, scope: core.App, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # <1>
        table = ddb.Table(
            self, "SimpleTable",
            partition_key=ddb.Attribute(
                name="item_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        core.CfnOutput(self, "TableName", value=table.table_name)

app = core.App()
SimpleDynamoDb(
    app, "SimpleDynamoDb",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)
app.synth()
