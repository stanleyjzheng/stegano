from flask import Flask, request

app = Flask(__name__)


@app.route("/api")
def hello():
    return "hello"


@app.route("/api/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        print(request.data)
        return "Image Upload Successful!"