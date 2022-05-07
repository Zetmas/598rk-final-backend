from flask import Flask, request
from twitter_analysis import analyze_tweet_account

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    return "working!"


@app.route("/analyze", methods=["GET"])
def analyze():
    args = request.args
    id = args["id"]
    result = analyze_tweet_account(id)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
