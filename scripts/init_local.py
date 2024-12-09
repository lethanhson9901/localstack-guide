import sys
from typing import Optional
from typer import Typer, Option
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
app = Typer()

@app.command()
def init_infrastructure(
    region: Optional[str] = Option(default="us-east-1", help="AWS region to use")
) -> None:
    """Initialize basic infrastructure in LocalStack."""
    from aws_local_dev.configs import AWSConfig

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        aws = AWSConfig(region=region, endpoint_url="http://localhost:4566")

        # Initialize S3
        task = progress.add_task("Creating S3 bucket...", total=None)
        s3 = aws.get_client("s3")
        try:
            if region == "us-east-1":
                s3.create_bucket(Bucket="my-application-storage")
            else:
                s3.create_bucket(
                    Bucket="my-application-storage",
                    CreateBucketConfiguration={"LocationConstraint": region}
                )
            progress.update(task, description="[green]Created S3 bucket successfully!")
        except s3.exceptions.BucketAlreadyExists:
            progress.update(task, description="[yellow]S3 bucket already exists")

        # Initialize DynamoDB
        task = progress.add_task("Creating DynamoDB table...", total=None)
        dynamodb = aws.get_client("dynamodb")
        try:
            dynamodb.create_table(
                TableName="users",
                KeySchema=[
                    {"AttributeName": "user_id", "KeyType": "HASH"},
                    {"AttributeName": "email", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "user_id", "AttributeType": "S"},
                    {"AttributeName": "email", "AttributeType": "S"},
                ],
                BillingMode="PAY_PER_REQUEST",
            )
            progress.update(task, description="[green]Created DynamoDB table successfully!")
        except dynamodb.exceptions.ResourceInUseException:
            progress.update(task, description="[yellow]DynamoDB table already exists")

if __name__ == "__main__":
    app()