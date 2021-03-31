#!/usr/bin/env python3
import os

import aws_cdk.core as cdk

from cdk.cdk_stack import CdkStack
from resource_stack_dvp.custom_vpc import VPCStackDVP
from resource_stack_dvp.custom_ec2 import EC2StackDVP

app = cdk.App()

envvar = cdk.Environment(account="568048966980", region="ap-south-1")

CdkStack(app, "CdkStack")

VPCStackDVP(app, "dvp-vpc-stack")

EC2StackDVP(app, "dvp-ec2-stack", env=envvar)

app.synth()
