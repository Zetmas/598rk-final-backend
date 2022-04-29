import tweepy
import json
import os

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

TWEET_COUNT = 15
USER_ID = "Brandooboomin"

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
