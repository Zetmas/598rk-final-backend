import re
import matplotlib.pyplot as plt
import json

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("vader_lexicon")




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
tweets = json.loads(open("data/" + data_folder_name + "/tweet_text.json", "r").read())

# Remove stopwords
tweets = [remove_stopword(tweet) for tweet in tweets]

with open(
    "analysis_result/" + data_folder_name + "/sanitized_tweets.json", "w"
) as outfile:
    json.dump(tweets, outfile)

tweet_blob = " ".join(tweets)
positive_tweets = []
neutral_tweets = []
negative_tweets = []

tweets_count = len(tweets)
positive_count = 0
neutral_count = 0
negative_count = 0

sia = SentimentIntensityAnalyzer()

for tweet in tweets:
    score = sia.polarity_scores(tweet)
    compound_score = score["compound"]

    if compound_score >= 0.05:
        positive_tweets.append(tweet)
        positive_count += 1
    elif compound_score > -0.05:
        neutral_tweets.append(tweet)
        neutral_count += 1
    else:
        negative_tweets.append(tweet)
        negative_count += 1

blob_scores = sia.polarity_scores(tweet_blob)
blob_pos = blob_scores["pos"]
blob_neu = blob_scores["neu"]
blob_neg = blob_scores["neg"]
blob_compound = blob_scores["compound"]

# Plot the sentiment analysis result
plot1_labels = "Positive", "Neutral", "Negative"
plot1_sizes = [positive_count, neutral_count, negative_count]
plot2_labels = "Positive", "Neutral", "Negative"
plot2_sizes = [blob_pos, blob_neu, blob_neg]

fig, axs = plt.subplots(2)
axs[0].pie(plot1_sizes, labels=plot1_labels, autopct="%1.1f%%", startangle=90)
axs[0].axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
axs[0].title.set_text("Tweets sentiment categorization")

axs[1].pie(plot2_sizes, labels=plot2_labels, autopct="%1.1f%%", startangle=90)
axs[1].axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
axs[1].title.set_text(
    "Overall sentiment composition.\nCompound score: {0}".format(blob_compound)
)

fig.tight_layout()

plt.savefig("analysis_result/" + data_folder_name + "/sentiment_analysis_result.png")
plt.close(fig