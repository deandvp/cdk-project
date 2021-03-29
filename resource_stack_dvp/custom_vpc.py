from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as _ec2

class ResourcesStackDVP(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dvp_configs = self.node.try_get_context('resourceconfig')['vpc_configs']

        custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            cidr=dvp_configs['vpc_cidr'],
            max_azs=2,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicsubnet",
                    cidr_mask=dvp_configs['cidr_mask'],
                    subnet_type=_ec2.SubnetType.PUBLIC
                )
            ]
        )

        cdk.CfnOutput(
            self,
            "customVPCIdOutput",
            value=custom_vpc.vpc_id,
            export_name="dvpVpcId"
        )