from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
import os

class MyFirstEc2(Stack):

    def __init__(self, scope: Construct, construct_id: str, key_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # <1>
        vpc = ec2.Vpc(
            self, "MyFirstEc2-Vpc",
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

        # <2>
        sg = ec2.SecurityGroup(
            self, "MyFirstEc2Vpc-Sg",
            vpc=vpc,
            allow_all_outbound=True,
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
        )

        # <3>
        host = ec2.Instance(
            self, "MyFirstEc2Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg,
            key_name=key_name
        )

        # print the server address
        cdk.CfnOutput(self, "InstancePublicDnsName", value=host.instance_public_dns_name)
        cdk.CfnOutput(self, "InstancePublicIp", value=host.instance_public_ip)

app = cdk.App()
MyFirstEc2(
    app, "MyFirstEc2",
    key_name=app.node.try_get_context("key_name"),
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

app.synth()
