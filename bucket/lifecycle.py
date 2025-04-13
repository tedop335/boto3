from botocore.exceptions import ClientError

def set_lifecycle_policy(s3_client, bucket_name, lifecycle_policy):
    """Sets a lifecycle policy for the specified S3 bucket."""
    try:
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )
    except ClientError as e:
        raise e