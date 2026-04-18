from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_dynamodb as ddb
)
import os

class SimpleDynamoDb(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # <1>
        table = ddb.Table(
            self, "SimpleTable",
            partition_key=ddb.Attribute(
                name="item_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        cdk.CfnOutput(self, "TableName", value=table.table_name)

app = cdk.App()
SimpleDynamoDb(
    app, "SimpleDynamoDb",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)
app.synth()
