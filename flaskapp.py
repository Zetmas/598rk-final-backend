from flask import Flask, request, url_for
from twitter_analysis import analyze_tweet_account, clear_cache
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    return "working!"


@app.route("/analyze", methods=["GET"])
def analyze():
    args = request.args
    id = args["id"]
    result = analyze_tweet_account(id)

    response = app.response_class(
        response=json.dumps(result), status=200, mimetype="application/json"
    )
    return response


@app.route("/clear", methods=["GET"])
def clear():
    clear_cache()
    return "Cache Cleared"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=105)
