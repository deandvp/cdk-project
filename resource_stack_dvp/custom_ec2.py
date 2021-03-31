from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_iam as _iam
class EC2StackDVP(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Importing existing Default VPC into Stack
        vpcimport = _ec2.Vpc.from_lookup(
            self,
            "DefaultVPCImported",
            vpc_id="vpc-f5b64e9e"
        )

        # Get latest linux Image and store it in a variable
        amazonLinuxAMI = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # Get latest Windows Image and store in a variable
        amazonWindowsAMI = _ec2.MachineImage.latest_windows(
            version = _ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_CORE_BASE
        )

        # Reading Bootstrap script
        with open("bootstrap_scripts/installhttpd.sh", mode="r") as file:
            userdatahttpd = file.read()

        # EC2 Instance Creation    
        webec2 = _ec2.Instance(
            self,
            "ec2instance1",
            instance_type=_ec2.InstanceType(
                instance_type_identifier="t2.micro"),
            instance_name="LinuxInstance-FreeTier",
            machine_image=_ec2.MachineImage.generic_linux(
               {"ap-south-1": "ami-0bcf5425cdc1d8a85"}
             ),
            #Enable to get the latest AMI and choose between Linux/Windows. MIGHT COST YOU!!
            # machine_image=amazonWindowsAMI,
            vpc=vpcimport,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC
            ),    
            user_data=_ec2.UserData.custom(userdatahttpd)
            )
        
        #Add EBS Volumes to the EC2 instance
        webec2.instance.add_property_override(
            "BlockDeviceMappings", [
                {
                    "DeviceName": "/dev/sdb",
                    "Ebs": {
                        "VolumeSize": "8",
                        "VolumeType": "io1",
                        "Iops": "400",
                        "DeleteOnTermination": "true"
                    }
                }
            ]
        )

        #Output the external IP of the Instance created
        ec2outputVar = cdk.CfnOutput(
            self,
            "ExternalIpOutput",
            description="Web Server's Public IP address",
            value=f"http://{webec2.instance_public_ip}"
            )
            
        # Update Secrity Group Inbound to allow all traffic in Port 80
        webec2.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), 
            description="Allow Web Traffic at 80"
        )

        # Add policies to the instance profile being created
        webec2.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )


