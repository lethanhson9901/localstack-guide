import logging
from collections.abc import Generator

import pytest
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_s3.client import S3Client

from aws_local_dev.configs import AWSConfig

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def aws_config() -> AWSConfig:
    """Provide AWS configuration for tests."""
    return AWSConfig()


@pytest.fixture(scope="session")
def s3_client(aws_config: AWSConfig) -> S3Client:
    """Provide S3 client for tests."""
    return aws_config.get_s3_client()


@pytest.fixture(scope="session")
def dynamodb_client(aws_config: AWSConfig) -> DynamoDBClient:
    """Provide DynamoDB client for tests."""
    return aws_config.get_dynamodb_client()


@pytest.fixture(autouse=True)
def cleanup_resources(
    s3_client: S3Client, dynamodb_client: DynamoDBClient
) -> Generator[None, None, None]:
    """Clean up test resources after each test."""
    yield

    # Clean up S3 buckets
    try:
        response = s3_client.list_buckets()
        for bucket in response["Buckets"]:
            s3_client.delete_bucket(Bucket=bucket["Name"])
    except Exception as e:
        logger.warning("Failed to clean up S3 buckets: %s", str(e))

    # Clean up DynamoDB tables
    try:
        response = dynamodb_client.list_tables()
        for table in response["TableNames"]:
            dynamodb_client.delete_table(TableName=table)
    except Exception as e:
        logger.warning("Failed to clean up DynamoDB tables: %s", str(e))
