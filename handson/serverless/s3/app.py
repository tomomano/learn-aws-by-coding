from aws_cdk import (
    core,
    aws_s3 as s3
)
import os

class SimpleS3(core.Stack):

    def __init__(self, scope: core.App, name: str, **kwargs) -> None:
        super().__init__(scope, name, **kwargs)

        # S3 bucket to store data
        bucket = s3.Bucket(
            self, "bucket",
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        core.CfnOutput(self, "BucketName", value=bucket.bucket_name)

app = core.App()
SimpleS3(
    app, "SimpleS3",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)
app.synth()
