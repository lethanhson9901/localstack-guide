from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_s3 as s3
from constructs import Construct


class BaseInfrastructureStack(Stack):
    """Base infrastructure stack for local development."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        """Initialize base infrastructure stack."""
        super().__init__(scope, construct_id, **kwargs)

        self._create_storage()
        self._create_database()

    def _create_storage(self) -> None:
        """Create S3 storage with security best practices."""
        self.storage_bucket = s3.Bucket(
            self,
            "StorageBucket",
            bucket_name="my-application-storage",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                    max_age=3000,
                )
            ],
        )

    def _create_database(self) -> None:
        """Create DynamoDB table with best practices."""
        self.user_table = dynamodb.Table(
            self,
            "UserTable",
            table_name="users",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name="email",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            time_to_live_attribute="ttl",
        )
