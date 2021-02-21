from flask import Flask, request
import os
import re
from google.cloud import storage

app = Flask(__name__)


@app.route("/api")
def hello():
    return "hello"


@app.route("/api/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        print("processing....")
        # TODO: insert pytorch function here!

        image_file = request.files["file"]
        upload_blob(image_file)
        return "Image Uploaded Successfully"
        # image_file.save(os.path.join("./public/images", image_file_name))
        # return {
        #     "message": "Image Upload Successful!",
        #     "imageSrc": f"./images/{image_file_name}",
        # }


def upload_blob(bucket_name="stego-upload-bucket", source_file):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    destination_blob_name = (
        re.sub("(\.png|\.jpg)", "", source_file.filename) + "-stego.png"
    )
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(source_file)

    print("File {} uploaded to {}.".format(source_file.filename, destination_blob_name))
