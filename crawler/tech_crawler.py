import os
import pytz
import tweepy
import datetime
import json
from twitter_app_keys import *


class Model:

    def __init__(self, uid, text, author, creation_date, lang, fav_count, location):
        self.text = text
        self.author = author
        self.creation_date = creation_date
        self.lang = lang
        self.fav_count = fav_count
        self.uid = uid
        self.location = location


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Model):
            return {"id": obj.uid,
            "text": obj.text,
            "author": obj.author,
            "creation_date": obj.creation_date,
            "lang": obj.lang,
            "fav_count": obj.fav_count,
            "location": obj.location}

            return json.JSONEncoder.default(self, obj)

def crawl(twitter_handle):

    print 'crawling tweets from ', twitter_handle

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    result = []
    api = tweepy.API(auth)
    page = 1

    while True:
        print 'crawling page number ', page, ' of', twitter_handle

        tweets = api.user_timeline(twitter_handle, count=150, page=page)


        for tweet in tweets:
            uid = tweet.id
            text = tweet.text
            author = tweet.author.name
            creation_date = tweet.created_at.isoformat() + 'Z'
            lang = tweet.lang
            fav_count = tweet.favorite_count

            if twitter_handle == "e27co":
                location = "1.3521,103.8198"
            else:
                location = "34.0522,-118.2437"

            data = Model(uid, text, author, creation_date, lang, fav_count, location)
            result.append(data)

        page += 1
        print 'crawled ', len(tweets), ' tweets'

        if len(tweets) == 0:
            break

    tweets_json = json.dumps(result, cls=Encoder)



    if not os.path.exists('tweets_data/'):
        os.makedirs('tweets_data/')

    f = open('tweets_data/' + twitter_handle + '_data.json', 'w')
    f.write(tweets_json)
    f.close()

    return tweets_json

if __name__ == "__main__":
    crawl('TechCrunch')
    crawl('WIRED')
    crawl('mashabletech')
    crawl('pogue')
    crawl('e27co')
