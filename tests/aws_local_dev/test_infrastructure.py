from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_s3.client import S3Client


def test_s3_bucket_exists(s3_client: S3Client) -> None:
    """Test S3 bucket creation."""
    buckets = s3_client.list_buckets()["Buckets"]
    assert any(b["Name"] == "my-application-storage" for b in buckets)


def test_s3_bucket_versioning(s3_client: S3Client) -> None:
    """Test S3 bucket versioning."""
    response = s3_client.get_bucket_versioning(Bucket="my-application-storage")
    assert response.get("Status") == "Enabled"


def test_dynamodb_table_exists(dynamodb_client: DynamoDBClient) -> None:
    """Test DynamoDB table creation."""
    tables = dynamodb_client.list_tables()["TableNames"]
    assert "users" in tables


def test_dynamodb_table_schema(dynamodb_client: DynamoDBClient) -> None:
    """Test DynamoDB table schema."""
    table = dynamodb_client.describe_table(TableName="users")["Table"]
    assert any(key["AttributeName"] == "user_id" for key in table["KeySchema"])
    assert any(key["AttributeName"] == "email" for key in table["KeySchema"])
