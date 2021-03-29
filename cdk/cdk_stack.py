from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (
    aws_s3 as _s3,
    core
)


class CdkStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        variableB = _s3.Bucket(
            self,
            "myBucketId",
            bucket_name = "dvpbucket512",
            versioned=False,
            encryption=_s3.BucketEncryption.S3_MANAGED,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL            
        )

        bucketvar = _s3.Bucket(
            self,
            "bucketvar"
        )

        print(bucketvar.bucket_name)

        print(variableB.bucket_name)

        buckoutput = core.CfnOutput(
            self,
            "FirstBucketOutput",
            value=bucketvar.bucket_name,
            description=f"My first bucket output",
            export_name="FirstBucketOpt"
        )
