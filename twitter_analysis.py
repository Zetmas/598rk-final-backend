import tweepy
import json
import os
import re
import matplotlib.pyplot as plt

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("vader_lexicon")

# consumer_key = "EGsp3o1XooukOJKSHVeZ2UTkn"
# consumer_secret = "1BpI7AdLz4epAQdMsELIu3qJsBiNlimrN8jZjZ3mU3liZgADdY"
# access_token = "2392107032-1AxBsFmdqhWMHggzbpEEpXAAAymumCycP1i3SXO"
# access_token_secret = "77FHYbYQpLBRzpdEBV5VgGXAdAskdXQ7e4SFVzuUHkG6T"

consumer_key = "GyqWsKLuqKUSSGqeY55cJhoyf"
consumer_secret = "VeEDGjjuj7lQQKITXCYvjPzJTy5sKm5MdYtHfsihWDjCt6yuE3"
access_token = "1506342078372106244-QGjUI8wBwLxVtLDTMMOskB6KaAdBXS"
access_token_secret = "3Itv4JYPAKmX0Ut5qhpmiUzgHNW7Armw5koyCn6nVOKgQ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

USER_ID = "notbillzo"

TWEET_COUNT = 20

depth = 0

# Depth 0
user_ids = [USER_ID]

for id in user_ids:
    path0 = "analysis_result/{0}".format(id, depth)
    path1 = "analysis_result/{0}/{1}".format(id, depth)
    if not os.path.exists(path0):
        os.makedirs(path0)
    if not os.path.exists(path1):
        os.makedirs(path1)

    follower_list = api.get_follower_ids(screen_name=id)
    followers = []
    # printing the latest 20 followers of the user
    for follower in follower_list:
        followers.append(follower)
    with open(
        "analysis_result/{0}/{1}/followers.json".format(id, depth), "w"
    ) as outfile:
        json.dump(followers, outfile)

    following_list = api.get_friend_ids(screen_name=id)
    followings = []
    for follower in following_list:
        followings.append(follower)
    with open(
        "analysis_result/{0}/{1}/followings.json".format(id, depth), "w"
    ) as outfile:
        json.dump(followings, outfile)

    tweets = api.user_timeline(
        screen_name=id,
        count=15,
        include_rts=False,
        tweet_mode="extended",
    )

    tweet_list = []
    for info in tweets:
        tweet_list.append(info.full_text)
    with open("analysis_result/{0}/{1}/tweets.json".format(id, depth), "w") as outfile:
        json.dump(tweet_list, outfile)

# Depth 1
depth = 1

followers = json.loads(
    open("analysis_result/{0}/{1}/followers.json".format(USER_ID, 0), "r").read()
)
followers = followers[:3]

followings = json.loads(
    open("analysis_result/{0}/{1}/followings.json".format(USER_ID, 0), "r").read()
)
followings = followings[:3]

user_ids = followers + followings

for id in user_ids:
    path0 = "analysis_result/{0}/1".format(USER_ID)
    path1 = "analysis_result/{0}/1/{1}".format(USER_ID, id)
    if not os.path.exists(path0):
        os.makedirs(path0)
    if not os.path.exists(path1):
        os.makedirs(path1)

    follower_list = api.get_follower_ids(user_id=id)
    followers = []
    # printing the latest 20 followers of the user
    for follower in follower_list:
        followers.append(follower)
    with open(
        "analysis_result/{0}/1/{1}/followers.json".format(USER_ID, id), "w"
    ) as outfile:
        json.dump(followers, outfile)

    following_list = api.get_friend_ids(user_id=id)
    followings = []
    for follower in following_list:
        followings.append(follower)
    with open(
        "analysis_result/{0}/1/{1}/followings.json".format(USER_ID, id), "w"
    ) as outfile:
        json.dump(followings, outfile)

    tweets = api.user_timeline(
        user_id=id,
        count=15,
        include_rts=False,
        tweet_mode="extended",
    )

    tweet_list = []
    for info in tweets:
        tweet_list.append(info.full_text)
    with open(
        "analysis_result/{0}/1/{1}/tweets.json".format(USER_ID, id), "w"
    ) as outfile:
        json.dump(tweet_list, outfile)


# Sentiment analysis part


def remove_stopword(text):
    stopword = nltk.corpus.stopwords.words("english")
    text = re.sub(r"http\S+", "url", text)
    text = text.encode("ascii", "ignore").decode()
    wordnet_lemmatizer = WordNetLemmatizer()
    result = [
        wordnet_lemmatizer.lemmatize(word.lower(), pos="v")
        for word in nltk.word_tokenize(text)
    ]
    # print(result)
    a = [
        word
        for word in result
        if word not in stopword and not bool(re.search(r"\d", text))
    ]
    return " ".join(a)


data_analysis_list = []

# read tweets from data/data_folder_name/tweets.txt
tweets = json.loads(
    open("analysis_result/{0}/0/tweets.json".format(USER_ID), "r").read()
)

community_tweets = []

rootdir = "analysis_result/{0}/1".format(USER_ID)

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == "tweets.json":
            community_tweets_portion = json.loads(
                open(os.path.join(subdir, file), "r").read()
            )
            community_tweets += community_tweets_portion

# Remove stopwords
tweets = [remove_stopword(tweet) for tweet in tweets]
community_tweets = [remove_stopword(tweet) for tweet in community_tweets]

tweet_blob = " ".join(tweets)
community_tweet_blob = " ".join(community_tweets)


sia = SentimentIntensityAnalyzer()

blob_scores = sia.polarity_scores(tweet_blob)
blob_pos = blob_scores["pos"]
blob_neu = blob_scores["neu"]
blob_neg = blob_scores["neg"]
blob_compound = blob_scores["compound"]

plot2_labels = "Positive", "Neutral", "Negative"
plot2_sizes = [blob_pos, blob_neu, blob_neg]

fig, axs = plt.subplots()

axs.pie(plot2_sizes, labels=plot2_labels, autopct="%1.1f%%", startangle=90)
axs.axis("equal")
axs.title.set_text("Individual Sentiment.\nCompound score: {0}".format(blob_compound))
fig.tight_layout()

plt.savefig("analysis_result/{0}/individual_analysis.png".format(USER_ID))
plt.close(fig)


blob_scores = sia.polarity_scores(community_tweet_blob)
blob_pos = blob_scores["pos"]
blob_neu = blob_scores["neu"]
blob_neg = blob_scores["neg"]
blob_compound = blob_scores["compound"]

plot2_labels = "Positive", "Neutral", "Negative"
plot2_sizes = [blob_pos, blob_neu, blob_neg]

fig, axs = plt.subplots()
axs.pie(plot2_sizes, labels=plot2_labels, autopct="%1.1f%%", startangle=90)
axs.axis("equal")
axs.title.set_text("Community Sentiment.\nCompound score: {0}".format(blob_compound))
fig.tight_layout()
plt.savefig("analysis_result/{0}/community_analysis.png".format(USER_ID))
plt.close(fig)
