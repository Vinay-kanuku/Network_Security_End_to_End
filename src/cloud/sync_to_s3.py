import os 
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from constant.training_pipeline import S3_ARTIFACT_PREFIX, LOCAL_ARTIFACT_DIR, S3_BUCKET_NAME
 
def upload_directory_to_s3(local_directory: str, bucket_name: str, s3_prefix: str):
    """
    Uploads a directory to an S3 bucket.
    Args:
        local_directory (str): The local directory to upload.
        bucket_name (str): The name of the S3 bucket.
        s3_prefix (str): The S3 prefix (folder) to upload to.
    """
    s3_client = boto3.client('s3')
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(s3_prefix, relative_path)
            try:
                s3_client.upload_file(local_path, bucket_name, s3_path)
                print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")
            except ClientError as e:
                print(f"Failed to upload {local_path}: {e}")
            except NoCredentialsError:
                print("Credentials not available.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Upload the local artifact directory to S3
    upload_directory_to_s3(LOCAL_ARTIFACT_DIR, S3_BUCKET_NAME, S3_ARTIFACT_PREFIX)
    # Upload the final model to S3

