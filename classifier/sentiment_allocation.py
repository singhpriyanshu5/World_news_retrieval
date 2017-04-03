import json
import urllib
from utility import TWEET_LIMIT

def sentiment_api(tweets_file, max_tweets):
    print 'Getting the sentiment value for ', tweets_file

    with open('tweets_data/' + tweets_file + '_data.json') as json_file:
        tweets = json.load(json_file)

    # do sentiment analysis
    for index, tweet in enumerate(tweets):
        ## Getting the sentiment labels for the first 20 files
        if max_tweets != None and index == max_tweets:
            print 'processing: %.2f%%' % (float(index) / len(tweets) * 100.0)
            break

        text = tweet['text'].encode('ascii', 'ignore')
        data = urllib.urlencode({'text': text})
        result = urllib.urlopen('http://text-processing.com/api/sentiment/', data)
        json_data = json.loads(result.read())
        tweet['label'] = json_data['label']

    with open('tweets_data/' + tweets_file + '_sentiments.json', 'w') as tweets_sentiments_file:
        if max_tweets != None:
            json.dump(tweets[:max_tweets], tweets_sentiments_file)
        else:
            json.dump(tweets, tweets_sentiments_file)


if __name__ == '__main__':
    sentiment_api('TechCrunch', TWEET_LIMIT)
