import os
from google.cloud import storage
import json
from resources import config

def upload_to_gcs(bucket_name, destination_blob_name, data):
    """
    Upload data to Google Cloud Storage.

    :param bucket_name: The name of the GCS bucket.
    :param destination_blob_name: The name of the file in GCS.
    :param data: The data to be uploaded, in dictionary format.
    """
    # Set the Google application credentials environment variable
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.CREDENTIAL_PATH
    # Initialize a Google Cloud Storage client
    client = storage.Client()
    # Get the bucket object
    bucket = client.bucket(bucket_name)
    # Get the blob object, which represents a file in the bucket
    blob = bucket.blob(destination_blob_name)
    # Convert the dictionary data to JSON format
    json_data = json.dumps(data)
    # Upload the JSON data as a string with the application/json content type
    blob.upload_from_string(json_data, content_type='application/json')
    # Print a confirmation message
    print(f"File {destination_blob_name} uploaded to {bucket_name}.")


def upload_to_local(directory_path, filename, data):
    """
    Upload data to Google Cloud Storage.

    :param bucket_name: The name of the GCS bucket.
    :param destination_blob_name: The name of the file in GCS.
    :param data: The data to be uploaded, in dictionary format.
    """
    # Ensure the provided data is a dictionary
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")

    # Construct the full file path
    file_path = os.path.join(directory_path, filename)

    # Ensure the filename ends with .json
    if not filename.lower().endswith('.json'):
        raise ValueError("Filename must end with .json")

    # Writing the JSON data to the specified file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

    print(f"JSON data has been saved to {file_path}.")