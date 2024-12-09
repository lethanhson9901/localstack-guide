import os
from dataclasses import dataclass, field
from typing import Literal, TypeVar, cast, overload

import boto3
from boto3.resources.base import ServiceResource
from botocore.client import BaseClient
from botocore.config import Config
from dotenv import load_dotenv
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_s3 import S3ServiceResource
from mypy_boto3_s3.client import S3Client

load_dotenv()

ResourceType = TypeVar("ResourceType", bound=ServiceResource)


@dataclass(frozen=True)
class AWSConfig:
    """AWS configuration with best practices and type safety."""

    region: str = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    endpoint_url: str = f"http://{os.getenv('LOCALSTACK_HOSTNAME', 'localhost')}:4566"
    _client_cache: dict[str, BaseClient] = field(default_factory=dict)
    _resource_cache: dict[str, ServiceResource] = field(default_factory=dict)

    @property
    def credentials(self) -> dict[str, str]:
        """Get AWS credentials for local development."""
        return {
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", "test"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        }

    @property
    def boto3_config(self) -> Config:
        """Get boto3 configuration with reasonable defaults."""
        return Config(
            retries={"max_attempts": 2, "mode": "standard"},
            connect_timeout=5,
            read_timeout=5,
            parameter_validation=True,
            max_pool_connections=10,
        )

    def get_client(self, service_name: Literal["s3", "dynamodb"]) -> BaseClient:
        """Get cached boto3 client."""
        if service_name not in self._client_cache:
            self._client_cache[service_name] = boto3.client(
                service_name,
                endpoint_url=self.endpoint_url,
                region_name=self.region,
                config=self.boto3_config,
                aws_access_key_id=self.credentials["aws_access_key_id"],
                aws_secret_access_key=self.credentials["aws_secret_access_key"],
            )
        return self._client_cache[service_name]

    @overload
    def get_resource(self, service_name: Literal["s3"]) -> S3ServiceResource: ...

    @overload
    def get_resource(self, service_name: Literal["dynamodb"]) -> DynamoDBServiceResource: ...

    def get_resource(
        self, service_name: Literal["s3", "dynamodb"]
    ) -> S3ServiceResource | DynamoDBServiceResource:
        """Get cached boto3 resource."""
        if service_name not in self._resource_cache:
            # Explicitly specify credentials instead of using **kwargs
            self._resource_cache[service_name] = boto3.resource(
                service_name,
                endpoint_url=self.endpoint_url,
                region_name=self.region,
                config=self.boto3_config,
                aws_access_key_id=self.credentials["aws_access_key_id"],
                aws_secret_access_key=self.credentials["aws_secret_access_key"],
            )
        return cast(S3ServiceResource | DynamoDBServiceResource, self._resource_cache[service_name])

    def get_s3_client(self) -> S3Client:
        """Get typed S3 client."""
        return cast(S3Client, self.get_client("s3"))

    def get_dynamodb_client(self) -> DynamoDBClient:
        """Get typed DynamoDB client."""
        return cast(DynamoDBClient, self.get_client("dynamodb"))
