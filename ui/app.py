from flask import Flask, request
import os

app = Flask(__name__)


@app.route("/api")
def hello():
    return "hello"


@app.route("/api/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        print("processing....")
        # TODO: insert pytorch function here!

        # image_file = request.files["file"]
        # image_file_name = image_file.filename
        # image_file.save(os.path.join("./public/images", image_file_name))
        # return {
        #     "message": "Image Upload Successful!",
        #     "imageSrc": f"./images/{image_file_name}",
        # }
