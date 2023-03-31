from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_batch_alpha as batch_alpha,
    aws_iam as iam,
    aws_ecr as ecr,
)
import os

class SimpleBatch(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket to store data
        bucket = s3.Bucket(
            self, "bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        vpc = ec2.Vpc(
            self, "vpc",
            max_azs=1,
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/23"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        managed_env = batch_alpha.ComputeEnvironment(
            self, "managed-env",
            compute_resources=batch_alpha.ComputeResources(
                vpc=vpc,
                allocation_strategy=batch_alpha.AllocationStrategy.BEST_FIT,
                desiredv_cpus=0,
                maxv_cpus=64,
                minv_cpus=0,
                instance_types=[
                    ec2.InstanceType("g4dn.xlarge")
                ],
            ),
            managed=True,
            compute_environment_name=self.stack_name + "compute-env"
        )

        job_queue = batch_alpha.JobQueue(
            self, "job-queue",
            compute_environments=[
                batch_alpha.JobQueueComputeEnvironment(
                    compute_environment=managed_env,
                    order=100
                )
            ],
            job_queue_name=self.stack_name + "job-queue"
        )

        job_role = iam.Role(
            self, "job-role",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ecs-tasks.amazonaws.com")
            )
        )
        # allow read and write access to S3 bucket
        bucket.grant_read_write(job_role)

        # create a ECR repository to push Docker image
        repo = ecr.Repository(
            self, "repository",
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        job_def = batch_alpha.JobDefinition(
            self, "job-definition",
            container=batch_alpha.JobDefinitionContainer(
                image=ecs.ContainerImage.from_ecr_repository(repo),
                command=["python3", "main.py"],
                vcpus=4,
                gpu_count=1,
                memory_limit_mib=12000,
                job_role=job_role,
                environment={
                    "BUCKET_NAME": bucket.bucket_name
                }
            ),
            job_definition_name=self.stack_name + "job-definition",
            timeout=cdk.Duration.hours(2),
        )

app = cdk.App()
SimpleBatch(
    app, "SimpleBatch",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

app.synth()
