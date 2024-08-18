import os
from minio import Minio
from minio.error import S3Error

def upload_image(minio_client, bucket_name, object_name, file_path):
    try:
        # Ensure the bucket exists, or create it if it doesn't.
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        # Upload the image file to MinIO.
        minio_client.fput_object(bucket_name, object_name, file_path)

        print(f"Successfully uploaded {object_name} to {bucket_name}")
    except S3Error as e:
        print(f"Error uploading {object_name}: {e}")

# Replace these with your MinIO server details.
minio_endpoint = "localhost:9000"
minio_access_key = ""
minio_secret_key = ""

# Initialize the MinIO client.
minio_client = Minio(minio_endpoint, access_key=minio_access_key, secret_key=minio_secret_key, secure=False)

# Define the bucket name and the directory containing the images.
bucket_name = "trial"
image_directory = "D:\Raka\minio\Image\images"

# List all files in the directory and upload them to MinIO.
for f in os.listdir(image_directory):
    file_path = os.path.join(image_directory, f)
    print("0")
    upload_image(minio_client, bucket_name, f, file_path) 
    print("0")
print("1")


def upload_query_image(path):
    pass
