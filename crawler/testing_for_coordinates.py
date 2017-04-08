import tweepy
from twitter_app_keys import *
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

page = 1
t_count = 0
geo_tweets_list = []
while True:
    tweets = api.user_timeline("@timesofindia", count=200, page=page)
    if len(tweets) == 0:
        break
    t_count = t_count + len(tweets)
    for tweet in tweets:
        if tweet.coordinates is not None:
            geo_tweets_list.append(tweet)
    page = page + 1

print len(geo_tweets_list)
# print geo_tweets_list
print t_count
