import logging
import os
import mimetypes
from botocore.exceptions import ClientError
from auth import init_client
from bucket.crud import list_buckets, create_bucket, delete_bucket, bucket_exists
from bucket.lifecycle import set_lifecycle_policy
from object.crud import upload_file, upload_large_file
import argparse

# Define the argument parser
parser = argparse.ArgumentParser(
    description="CLI program to manage S3 buckets and objects.",
    usage='''
    Example usage:
    Upload a small file:
        python s3helper.py -bn my-bucket -sf /path/to/small-file.txt
    Upload a large file:
        python s3helper.py -bn my-bucket -lf /path/to/large-file.txt
    Set lifecycle policy:
        python s3helper.py -bn my-bucket -lp
    ''',
    prog='s3helper.py',
    epilog='DEMO APP FOR S3 MANAGEMENT'
)

# Add arguments
parser.add_argument("-bn", "--bucket_name", type=str, help="Name of the S3 bucket.", required=True)
parser.add_argument("-sf", "--small_file", type=str, help="Path to a small file to upload.", default=None)
parser.add_argument("-lf", "--large_file", type=str, help="Path to a large file to upload.", default=None)
parser.add_argument("-lp", "--lifecycle_policy", help="Set lifecycle policy to delete objects after 120 days.", action="store_true")

# Define the main function
def main():
    s3_client = init_client()
    args = parser.parse_args()

    if args.bucket_name:
        # Upload a small file
        if args.small_file:
            try:
                file_name = os.path.basename(args.small_file)
                s3_client.upload_file(args.small_file, args.bucket_name, file_name)
                print(f"Small file '{file_name}' uploaded successfully to bucket '{args.bucket_name}'.")
            except ClientError as e:
                logging.error(e)
                print(f"Failed to upload small file '{args.small_file}'.")

        # Upload a large file with optional MIME type validation
        if args.large_file:
            try:
                file_name = os.path.basename(args.large_file)
                mime_type, _ = mimetypes.guess_type(args.large_file)
                if mime_type:
                    print(f"Detected MIME type: {mime_type}")
                else:
                    print("MIME type could not be determined. Proceeding with upload.")
                s3_client.upload_file(args.large_file, args.bucket_name, file_name)
                print(f"Large file '{file_name}' uploaded successfully to bucket '{args.bucket_name}'.")
            except ClientError as e:
                logging.error(e)
                print(f"Failed to upload large file '{args.large_file}'.")

        # Set lifecycle policy
        if args.lifecycle_policy:
            try:
                lifecycle_policy = {
                    'Rules': [
                        {
                            'ID': 'DeleteAfter120Days',
                            'Filter': {'Prefix': ''},
                            'Status': 'Enabled',
                            'Expiration': {'Days': 120}
                        }
                    ]
                }
                set_lifecycle_policy(s3_client, args.bucket_name, lifecycle_policy)
                print(f"Lifecycle policy set for bucket '{args.bucket_name}' to delete objects after 120 days.")
            except ClientError as e:
                logging.error(e)
                print(f"Failed to set lifecycle policy for bucket '{args.bucket_name}'.")

if __name__ == "__main__":
    try:
        main()
    except ClientError as e:
        logging.error(e)