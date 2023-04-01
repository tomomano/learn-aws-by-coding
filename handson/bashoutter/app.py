from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_lambda as _lambda,
    aws_ssm as ssm,
    aws_apigateway as apigw,
)
import os

class Bashoutter(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # <1>
        # dynamoDB table to store haiku
        table = ddb.Table(
            self, "Bashoutter-Table",
            partition_key=ddb.Attribute(
                name="item_id",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # <2>
        bucket = s3.Bucket(
            self, "Bashoutter-Bucket",
            website_index_document="index.html",
            public_read_access=True,
            auto_delete_objects=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        common_params = {
            "runtime": _lambda.Runtime.PYTHON_3_7,
            "environment": {
                "TABLE_NAME": table.table_name
            }
        }

        # <3>
        # define Lambda functions
        get_haiku_lambda = _lambda.Function(
            self, "GetHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.get_haiku",
            memory_size=512,
            timeout=cdk.Duration.seconds(10),
            **common_params,
        )
        post_haiku_lambda = _lambda.Function(
            self, "PostHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.post_haiku",
            **common_params,
        )
        patch_haiku_lambda = _lambda.Function(
            self, "PatchHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.patch_haiku",
            **common_params,
        )
        delete_haiku_lambda = _lambda.Function(
            self, "DeleteHaiku",
            code=_lambda.Code.from_asset("api"),
            handler="api.delete_haiku",
            **common_params,
        )

        # <4>
        # grant permissions
        table.grant_read_data(get_haiku_lambda)
        table.grant_read_write_data(post_haiku_lambda)
        table.grant_read_write_data(patch_haiku_lambda)
        table.grant_read_write_data(delete_haiku_lambda)

        # <5>
        # define API Gateway
        api = apigw.RestApi(
            self, "BashoutterApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            )
        )

        haiku = api.root.add_resource("haiku")
        haiku.add_method(
            "GET",
            apigw.LambdaIntegration(get_haiku_lambda)
        )
        haiku.add_method(
            "POST",
            apigw.LambdaIntegration(post_haiku_lambda)
        )

        haiku_item_id = haiku.add_resource("{item_id}")
        haiku_item_id.add_method(
            "PATCH",
            apigw.LambdaIntegration(patch_haiku_lambda)
        )
        haiku_item_id.add_method(
            "DELETE",
            apigw.LambdaIntegration(delete_haiku_lambda)
        )

        # store parameters in SSM
        ssm.StringParameter(
            self, "TABLE_NAME",
            parameter_name="TABLE_NAME",
            string_value=table.table_name
        )
        ssm.StringParameter(
            self, "ENDPOINT_URL",
            parameter_name="ENDPOINT_URL",
            string_value=api.url
        )

        # Output parameters
        cdk.CfnOutput(self, 'BucketUrl', value=bucket.bucket_website_domain_name)

app = cdk.App()
Bashoutter(
    app, "Bashoutter",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

app.synth()
