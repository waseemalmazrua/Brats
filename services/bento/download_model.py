import os
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('brats-uploads')
blob = bucket.blob('models/brats_model.bentomodel')
blob.download_to_filename('/tmp/brats_model.bentomodel')
print("Model downloaded successfully")