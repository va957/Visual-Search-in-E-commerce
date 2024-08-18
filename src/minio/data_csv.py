import os
import cv2
import pandas as pd
import numpy as np

def main():

    # Specify the directory containing your images
    image_directory = 'test_images/'

    # Create an empty list to store image information
    image_data = []

    # Iterate through files in the directory
    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            file_path = os.path.join(image_directory, filename)
            image = cv2.imread(file_path)

            if image is not None:
                # Flatten the image into a 1D vector
                image_vector = image.flatten()
                
                # Append image information to the list
                image_data.append([filename, image_vector])

    # Create a DataFrame from the list
    df = pd.DataFrame(image_data, columns=['Image Name', 'Image Vector'])

    # Save the DataFrame to a CSV file
    csv_file = 'image_info_with_vectors.csv'
    df.to_csv(csv_file, index=False)

    print(f'Image information with vectors saved to {csv_file}.')

if __name__ == "__main__":
    main()