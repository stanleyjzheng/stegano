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
        imageFile = request.files["file"]
        imageFile.save(os.path.join("images", imageFile.filename))
        return "Image Upload Successful!"
