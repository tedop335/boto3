import boto3

def init_client():
    """Initializes and returns a boto3 S3 client."""
    return boto3.client('s3')