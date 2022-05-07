from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    return "working!"


@app.route("/analyze", methods=["GET"])
def analyze():
    args = request.args
    return args


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
