from botocore.exceptions import ClientError

def list_buckets(s3_client):
    """Lists all S3 buckets."""
    try:
        return s3_client.list_buckets()
    except ClientError as e:
        raise e

def create_bucket(s3_client, bucket_name, region=None):
    """Creates an S3 bucket."""
    try:
        if region:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        else:
            s3_client.create_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        raise e

def delete_bucket(s3_client, bucket_name):
    """Deletes an S3 bucket."""
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        raise e

def bucket_exists(s3_client, bucket_name):
    """Checks if an S3 bucket exists."""
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False