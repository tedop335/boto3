from botocore.exceptions import ClientError

def upload_file(s3_client, file_path, bucket_name, object_name):
    """Uploads a small file to S3."""
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        raise e

def upload_large_file(s3_client, file_path, bucket_name, object_name):
    """Uploads a large file to S3 using multipart upload."""
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        raise e