import os
import re
import matplotlib.pyplot as plt
import json

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("vader_lexicon")

USER_ID = "Brandooboomin"


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

plt.savefig("analysis_result/{0}/0/individual_analysis.png".format(USER_ID))
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
plt.savefig("analysis_result/{0}/0/community_analysis.png".format(USER_ID))
plt.close(fig)
