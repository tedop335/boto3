import logging
import argparse
from auth import init_client
from bucket.versioning import check_versioning, list_file_versions, restore_previous_version
from bucket.crud import list_buckets, create_bucket, delete_bucket, bucket_exists
from bucket.policy import assign_policy, read_bucket_policy
from bucket.encryption import set_bucket_encryption, read_bucket_encryption
from bucket.lifecycle import set_lifecycle_policy
from object.crud import upload_small_file, upload_large_file, get_objects, delete_object, download_file_and_upload_to_s3
from object.policy import set_object_access_policy

parser = argparse.ArgumentParser(description="AWS S3 CLI Tool")

parser.add_argument("-bn",
                    "--bucket_name",
                    type=str,
                    help="Name of the bucket to perform operations on.",
                    default=None)

parser.add_argument("-cb",
                    "--create_bucket",
                    action="store_true",
                    help="Create a new bucket.")

parser.add_argument("-db",
                    "--delete_bucket",
                    action="store_true",
                    help="Delete the specified bucket.")

parser.add_argument("-eb",
                    "--enable_bucket_encryption",
                    action="store_true",
                    help="Enable bucket encryption.")

parser.add_argument("-rbp",
                    "--read_bucket_policy",
                    action="store_true",
                    help="Read bucket policy.")

parser.add_argument("-sbp",
                    "--set_bucket_policy",
                    type=str,
                    help="Set bucket policy. Options: 'public_read_policy', 'multiple_policy'.",
                    default=None)

parser.add_argument("-slp",
                    "--set_lifecycle_policy",
                    action="store_true",
                    help="Set lifecycle policy for the bucket.")

parser.add_argument("-usf",
                    "--upload_small_file",
                    type=str,
                    help="Upload a small file to the bucket.",
                    default=None)

parser.add_argument("-ulf",
                    "--upload_large_file",
                    type=str,
                    help="Upload a large file to the bucket.",
                    default=None)

parser.add_argument("-dfo",
                    "--delete_file_object",
                    type=str,
                    help="Delete a file object from the bucket.",
                    default=None)

parser.add_argument("-dlu",
                    "--download_and_upload",
                    type=str,
                    help="Download a file from a URL and upload it to the bucket.",
                    default=None)

parser.add_argument("-go",
                    "--get_objects",
                    action="store_true",
                    help="List all objects in the bucket.")

parser.add_argument("-soa",
                    "--set_object_access",
                    type=str,
                    help="Set object access policy to public-read.",
                    default=None)

parser.add_argument("-bv",
                    "--bucket_versioning",
                    help="Check if versioning is enabled for the bucket.",
                    action="store_true")

parser.add_argument("-lfv",
                    "--list_file_versions",
                    type=str,
                    help="List versions of a specific file in the bucket.",
                    default=None)

parser.add_argument("-rpv",
                    "--restore_previous_version",
                    type=str,
                    help="Restore the previous version of a specific file in the bucket.",
                    default=None)

def main():
    s3_client = init_client()
    args = parser.parse_args()

    if args.bucket_name:
        if args.create_bucket:
            region = getenv("aws_region_name")
            if create_bucket(s3_client, args.bucket_name, region):
                print(f"Bucket {args.bucket_name} created successfully")
            else:
                print(f"Failed to create bucket {args.bucket_name}")

        if args.delete_bucket:
            if delete_bucket(s3_client, args.bucket_name):
                print(f"Bucket {args.bucket_name} deleted successfully")
            else:
                print(f"Failed to delete bucket {args.bucket_name}")

        if args.enable_bucket_encryption:
            if set_bucket_encryption(s3_client, args.bucket_name):
                print(f"Bucket encryption enabled for {args.bucket_name}")
            else:
                print(f"Failed to enable bucket encryption for {args.bucket_name}")

        if args.read_bucket_policy:
            policy = read_bucket_policy(s3_client, args.bucket_name)
            if policy:
                print(f"Bucket policy for {args.bucket_name}: {policy}")
            else:
                print(f"Failed to read bucket policy for {args.bucket_name}")

        if args.set_bucket_policy:
            assign_policy(s3_client, args.set_bucket_policy, args.bucket_name)

        if args.set_lifecycle_policy:
            if set_lifecycle_policy(s3_client, args.bucket_name):
                print(f"Lifecycle policy set for bucket {args.bucket_name}")
            else:
                print(f"Failed to set lifecycle policy for bucket {args.bucket_name}")

        if args.upload_small_file:
            if upload_small_file(s3_client, args.bucket_name, args.upload_small_file):
                print(f"File {args.upload_small_file} uploaded successfully to bucket {args.bucket_name}")
            else:
                print(f"Failed to upload file {args.upload_small_file} to bucket {args.bucket_name}")

        if args.upload_large_file:
            if upload_large_file(s3_client, args.bucket_name, args.upload_large_file):
                print(f"Large file {args.upload_large_file} uploaded successfully to bucket {args.bucket_name}")
            else:
                print(f"Failed to upload large file {args.upload_large_file} to bucket {args.bucket_name}")

        if args.delete_file_object:
            if delete_object(s3_client, args.bucket_name, args.delete_file_object):
                print(f"File {args.delete_file_object} deleted successfully from bucket {args.bucket_name}")
            else:
                print(f"Failed to delete file {args.delete_file_object} from bucket {args.bucket_name}")

        if args.download_and_upload:
            result = download_file_and_upload_to_s3(s3_client, args.bucket_name, args.download_and_upload)
            print(result)

        if args.get_objects:
            objects = get_objects(s3_client, args.bucket_name)
            if objects:
                print(f"Objects in bucket {args.bucket_name}: {objects}")
            else:
                print(f"No objects found in bucket {args.bucket_name}")

        if args.set_object_access:
            if set_object_access_policy(s3_client, args.bucket_name, args.set_object_access):
                print(f"Access policy set to public-read for object {args.set_object_access} in bucket {args.bucket_name}")
            else:
                print(f"Failed to set access policy for object {args.set_object_access} in bucket {args.bucket_name}")

        if args.bucket_versioning:
            versioning_status = check_versioning(s3_client, args.bucket_name)
            print(f"Bucket versioning status: {versioning_status}")

        if args.list_file_versions:
            versions = list_file_versions(s3_client, args.bucket_name, args.list_file_versions)
            if versions:
                print(f"Versions of file {args.list_file_versions}:")
                for version in versions:
                    print(f"  Version ID: {version['VersionId']}, Last Modified: {version['LastModified']}")
            else:
                print(f"No versions found for file {args.list_file_versions} in bucket {args.bucket_name}")

        if args.restore_previous_version:
            if restore_previous_version(s3_client, args.bucket_name, args.restore_previous_version):
                print(f"Previous version of file {args.restore_previous_version} restored successfully")
            else:
                print(f"Failed to restore the previous version of file {args.restore_previous_version}")

    else:
        buckets = list_buckets(s3_client)
        print("Buckets:")
        for bucket in buckets["Buckets"]:
            print(f"  {bucket['Name']}")

if __name__ == "__main__":
    main()
import boto3
from botocore.exceptions import ClientError


def check_versioning(aws_s3_client, bucket_name):
    try:
        response = aws_s3_client.get_bucket_versioning(Bucket=bucket_name)
        return response.get("Status", "Not Enabled")
    except ClientError as e:
        print(f"Error checking versioning for bucket {bucket_name}: {e}")
        return None


def list_file_versions(aws_s3_client, bucket_name, file_name):
    try:
        response = aws_s3_client.list_object_versions(Bucket=bucket_name, Prefix=file_name)
        if "Versions" in response:
            return response["Versions"]
        return []
    except ClientError as e:
        print(f"Error listing versions for file {file_name} in bucket {bucket_name}: {e}")
        return None


def restore_previous_version(aws_s3_client, bucket_name, file_name):
    try:
        versions = list_file_versions(aws_s3_client, bucket_name, file_name)
        if versions and len(versions) > 1:
            previous_version = versions[1]  # Assuming the second version is the previous one
            aws_s3_client.copy_object(
                Bucket=bucket_name,
                CopySource={
                    "Bucket": bucket_name,
                    "Key": file_name,
                    "VersionId": previous_version["VersionId"]
                },
                Key=file_name
            )
            return True
        return False
    except ClientError as e:
        print(f"Error restoring previous version for file {file_name} in bucket {bucket_name}: {e}")
        return False