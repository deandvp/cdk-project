#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from cdk.cdk_stack import CdkStack

from resource_stack_dvp.custom_vpc import VPCStackDVP
from resource_stack_dvp.custom_ec2 import EC2StackDVP

app = core.App()

envvar = core.Environment(account="568048966980", region="ap-south-1")

CdkStack(app, "CdkStack")

VPCStackDVP(app, "dvp-vpc-stack")

EC2StackDVP(app, "dvp-ec2-stack", env=envvar)

app.synth()
