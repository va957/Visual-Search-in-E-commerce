import numpy as np
import cv2
from pymilvus import Milvus, IndexType
import pickle
import configparser
from pymilvus import connections, utility, Collection
from keras.models import load_model
from keras import backend as K
from .models import QueryImage

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Model 
from sentence_transformers import SentenceTransformer
from PIL import Image
import re
import boto3
import os
import time
from PIL import Image
import numpy as np

def fetch_s3_images(request):
    latent_dim = 512
    images = QueryImage.objects.filter(user_id=request.user.id).values().latest('image_id')
    input_img = 'media/'+images['image_file']
    
    milvus_uri = ''
    token = ''
    connections.connect("default", uri=milvus_uri, token=token)
    print(f"Connecting to Milvus: {milvus_uri}")

    # Check if the collection exists
    collection_name = "embedding_500"
    check_collection = utility.has_collection(collection_name)
    
    #print(check_collection)
    
    search_params = {
        "metric_type": "IP", 
    }
    # Define the Milvus collection to store image embeddings

    collection_name = Collection("embedding_500")      # Get an existing collection.
    collection_name.load()

    model = SentenceTransformer("clip-ViT-B-32")

    # Preprocess and encode the query image
    # query_image_path = 'logo.jpeg'
    # query_image = cv2.imread(query_image_path)
    # query_image = cv2.resize(query_image, (64,64))  # Adjust dimensions as needed
    # query_image = np.array(query_image)
    # print(query_image.shape)
    # Assuming the encoder model is a Keras model, you can use it like this:
    query_image = Image.open(input_img)
    query_embedding = model.encode(query_image)
    query_embedding = [query_embedding.tolist()]

    results = collection_name.search(
        data=query_embedding, 
        anns_field="vector", 
        param=search_params,
        limit = 15
    )
    #print(results[0])
    image_id = []
    for i in results[0]:
        # Use regular expression to find the number following "id:"
        
        temp = int(str(i).split(',')[0][4:])
        image_id.append(str(temp) + '.jpg')
    
    # Replace these with your own AWS credentials
    aws_access_key_id = AWS_ACCESS_KEY_ID
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    region_name = AWS_S3_REGION_NAME
    bucket_name = AWS_STORAGE_BUCKET_NAME

    # Initialize the S3 client
    s3 = boto3.client('s3', region_name=region_name,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    # List the objects (images) in your S3 bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    #print(image_id)
    
    # Fetch images one by one    
    image_urls = []

    print(response.get('Contents', []))

    for obj in response.get('Contents', []):
        s3_object = obj['Key']
        # print(s3_object)
        if str(s3_object).startswith('Images/final_images/'):
            # print("check", s3)
            if s3_object[21:] in image_id:
                # Define a local file path to save the image
                user_id = request.user.id
                s3_object = str(s3_object[7:])
                s3_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_object}'
                image_urls.append(s3_url)

    return image_urls

# if __name__=="__main__":
#     main()
