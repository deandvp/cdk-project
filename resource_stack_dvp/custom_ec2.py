from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as _ec2

class EC2StackDVP(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_var=_ec2.Vpc.from_lookup(
            self,
            "importedVPC",
            vpc_id="vpc-f5b64e9e"
        )

        ec2_var=_ec2.Instance(
            self,
            "ec2instance1",
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t2.micro"),
            instance_name="linux instance",
            machine_image=_ec2.MachineImage.generic_linux(
                {"ap-south-1": "ami-0bcf5425cdc1d8a85"}
            ),
            vpc=vpc_var,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC
            )    
            )
        