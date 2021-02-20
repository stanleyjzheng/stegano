from flask import Flask

app = Flask(__name__)


@app.route("/api")
def hello():
    return "hello"


@app.route("/api/upload", requests=["POST"])
def upload():
    print("CALLED!")
    print(request.data)