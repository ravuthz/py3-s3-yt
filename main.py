import os
import boto3
import urllib.parse
import boto3.exceptions
import botocore.exceptions
from dotenv import load_dotenv

from youtube import upload_video

load_dotenv()

local_file_path = "/tmp/"
bucket_name = os.getenv('S3_BUCKET')
region_name = os.getenv('S3_REGION')
aws_access_key_id =  os.getenv('S3_ACCESS_KEY')
aws_secret_access_key = os.getenv('S3_SECRET_KEY')

yt_developerKey=os.getenv('YT_DEVELOPER_KEY')


# Create an S3 client
s3 = boto3.client("s3", 
    region_name=region_name, 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key)






# response = s3.list_objects(Bucket=bucket_name)
    # for obj in response['Contents']:
    #     print(obj['Key'])

def list_all_s3_files():
    result = s3.list_objects(Bucket=bucket_name)
    total_size = 0
    num_objects = 0

    while result.get("IsTruncated"):
        contents = result.get("Contents", [])
        total_size += sum(obj['Size'] for obj in contents)
        num_objects += len(contents)
        result = s3.list_objects(Bucket=bucket_name, Marker=result["Contents"][-1]["Key"])

    contents = result.get("Contents", [])
    # total_size += sum(obj['Size'] for obj in contents)

    for obj in contents:
        print(obj['Key'])
        total_size += obj['Size']

    num_objects += len(contents)

    print(f"Total size of objects in {bucket_name}: {total_size} bytes")
    print(f"Number of objects in {bucket_name}: {num_objects}")


def download_s3_file(file_name):
    local_file_name = local_file_path + file_name
    decoded_file_name = urllib.parse.unquote(file_name)
    # encoded_file_name = urllib.parse.quote(file_name)

    directory = os.path.dirname(local_file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
   
    try:
        s3.download_file(bucket_name, decoded_file_name, local_file_name)
    # except boto3.exceptions.S3DownloadException as e:
    #     if e.response['Error']['Code'] == "404":
    #         print("The file does not exist in the specified bucket and path.")
    #     else:
    #         raise
    except botocore.exceptions.ClientError as e:
        print("An error occurred during the download:", e)
    except Exception as e:
        print("An error occurred:", e)






# Example usage

file_name = "1667967444244_John Wick 2014.mp4"
# file_name = "(1994)/ch-01-42-1671215365587.mp4"


# list_all_s3_files()

# download_s3_file(file_name)

upload_video(local_file_path + file_name, file_name, file_name, "private")
