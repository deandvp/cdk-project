from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as _ec2

class EC2StackDVP(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Importing existing Default VPC into Stack
        vpc_var = _ec2.Vpc.from_lookup(
            self,
            "DefaultVPCImported",
            vpc_id="vpc-f5b64e9e"
        )
        # Reading Bootstrap script
        with open("bootstrap_scripts/installhttpd.sh", mode="r") as file:
            userdata_var = file.read()

        # EC2 Instance Creation    
        webec2_var = _ec2.Instance(
            self,
            "ec2instance1",
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t2.micro"),
            instance_name="LinuxInstance",
            machine_image=_ec2.MachineImage.generic_linux(
                {"ap-south-1": "ami-0bcf5425cdc1d8a85"}
            ),
            vpc=vpc_var,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC
            ),    
            user_data=_ec2.UserData.custom(userdata_var)
            )
        
        ec2outputVar = cdk.CfnOutput(
            self,
            "ExternalIpOutput",
            description="Web Server's Public IP address",
            value=f"http://{webec2_var.instance_public_ip}"
            )
            
        # Update Secrity Group Inbound to allow all traffic in Port 80
        webec2_var.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), 
            description="Allow Web Traffic at 80"
        )


