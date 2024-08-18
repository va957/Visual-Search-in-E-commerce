import boto3
import pandas as pd

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id='',
    aws_secret_access_key='+A'
)

# Create an empty list to store dictionaries
data = []

# Iterate through S3 objects and store the image IDs in the list
for obj in s3.Bucket('django-raka').objects.all():
    # Extract the image ID (file name) from the object key
    image_id = obj.key.split('/')[-1]
    
    # Append the image ID as a dictionary to the list
    data.append({'Image ID': image_id})

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

# Print the DataFrame
df.to_csv('image_id.csv')
