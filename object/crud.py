import json
import os
import requests
from boto3.s3.transfer import TransferConfig


def public_read_policy(bucket_name):
  policy = {
    "Version":
    "2012-10-17",
    "Statement": [{
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": f"arn:aws:s3:::{bucket_name}/*",
    }],
  }

  return json.dumps(policy)


def multiple_policy(bucket_name):
  policy = {
    "Version":
    "2012-10-17",
    "Statement": [{
      "Action": [
        "s3:PutObject", "s3:PutObjectAcl", "s3:GetObject", "s3:GetObjectAcl",
        "s3:DeleteObject"
      ],
      "Resource":
      [f"arn:aws:s3:::{bucket_name}", f"arn:aws:s3:::{bucket_name}/*"],
      "Effect":
      "Allow",
      "Principal":
      "*"
    }]
  }

  return json.dumps(policy)


def assign_policy(aws_s3_client, policy_function, bucket_name):
  policy = None
  if policy_function == "public_read_policy":
    policy = public_read_policy(bucket_name)
  elif policy_function == "multiple_policy":
    policy = multiple_policy(bucket_name)

  if (not policy):
    print('please provide policy')
    return

  aws_s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
  print("Bucket multiple policy assigned successfully")


def read_bucket_policy(aws_s3_client, bucket_name):
  policy = aws_s3_client.get_bucket_policy(Bucket=bucket_name)

  status_code = policy["ResponseMetadata"]["HTTPStatusCode"]
  if status_code == 200:
    return policy["Policy"]
  return False


def upload_small_file(aws_s3_client, bucket_name, file_path):
    file_name = os.path.basename(file_path)
    try:
        aws_s3_client.upload_file(file_path, bucket_name, file_name, ExtraArgs={'ACL': 'public-read'})
        return True
    except Exception as e:
        print(f"Failed to upload {file_name} to {bucket_name}: {e}")
        return False


def upload_large_file(aws_s3_client, bucket_name, file_path):
    file_name = os.path.basename(file_path)
    config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10, multipart_chunksize=1024 * 25, use_threads=True)
    aws_s3_client.upload_file(file_path, bucket_name, file_name, Config=config)
    return True


def download_file_and_upload_to_s3(aws_s3_client, bucket_name, file_url):
    file_name = file_url.split("/")[-1]
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        aws_s3_client.upload_file(file_name, bucket_name, file_name)
        os.remove(file_name)  # Clean up the local file after upload
        return f"File {file_name} uploaded successfully to bucket {bucket_name}"
    else:
        return f"Failed to download file from {file_url}. Status code: {response.status_code}"


def get_objects(aws_s3_client, bucket_name):
    response = aws_s3_client.list_objects_v2(Bucket=bucket_name)
    if "Contents" in response:
        return [obj["Key"] for obj in response["Contents"]]
    return []


def delete_object(aws_s3_client, bucket_name, file_name):
    try:
        response = aws_s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 204:
            return True
    except Exception as e:
        print(f"Error deleting file {file_name} from bucket {bucket_name}: {e}")
    return False
