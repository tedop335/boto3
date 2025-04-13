def check_versioning(aws_s3_client, bucket_name):
    response = aws_s3_client.get_bucket_versioning(Bucket=bucket_name)
    return response.get("Status", "Not Enabled")

def list_file_versions(aws_s3_client, bucket_name, file_name):
    response = aws_s3_client.list_object_versions(Bucket=bucket_name, Prefix=file_name)
    if "Versions" in response:
        return [
            {"VersionId": version["VersionId"], "LastModified": version["LastModified"]}
            for version in response["Versions"]
        ]
    return []

def restore_previous_version(aws_s3_client, bucket_name, file_name):
    versions = list_file_versions(aws_s3_client, bucket_name, file_name)
    if len(versions) > 1:
        previous_version_id = versions[1]["VersionId"]
        copy_source = {"Bucket": bucket_name, "Key": file_name, "VersionId": previous_version_id}
        aws_s3_client.copy_object(
            CopySource=copy_source,
            Bucket=bucket_name,
            Key=file_name
        )
        return True
    return False
