def set_lifecycle_policy(aws_s3_client, bucket_name):
    lifecycle_policy = {
        "Rules": [
            {
                "ID": "DeleteAfter120Days",
                "Filter": {"Prefix": ""},
                "Status": "Enabled",
                "Expiration": {"Days": 120},
            }
        ]
    }
    aws_s3_client.put_bucket_lifecycle_configuration(
        Bucket=bucket_name, LifecycleConfiguration=lifecycle_policy
    )
    return True
