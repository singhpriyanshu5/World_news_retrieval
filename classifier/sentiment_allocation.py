import json
import urllib
from utility import TWEET_LIMIT, handles_lst
API_KEY = '03a678d69796e8a821619eaa38714674ksB7JbwOKhU-5XWofHGa1edqg4AnDzrV'

def sentiment_api_mixed(num_tweets):
    # print 'Getting the sentiment value for ', tweets_file
    tweets_mixed = []
    for handle in handles_lst:
        with open('tweets_data/'+handle+'_data.json') as json_file:
            tweets = json.load(json_file)

            tweets = tweets[:(num_tweets/5)]
        # tweets_mixed.extend(tweets[:(num_tweets/5)])



        # do sentiment analysis
        for index, tweet in enumerate(tweets):
            ## Getting the sentiment labels for the first 20 files
            # if max_tweets != None and index == max_tweets:
            #     print 'processing: %.2f%%' % (float(index) / len(tweets) * 100.0)
            #     break
            if index%100 == 0:
                print 'done with {} tweets out of {}'.format(index+1,len(tweets_mixed))

            text = tweet['text'].encode('ascii', 'ignore')
            data= urllib.urlencode({'text':text, 'api-key':API_KEY})

            result = urllib.urlopen('https://api.sentigem.com/external/get-sentiment?', data)
            # result = urllib.urlopen('https://api.sentigem.com/external/get-sentiment?api-key=03a678d69796e8a821619eaa38714674ksB7JbwOKhU-5XWofHGa1edqg4AnDzrV&text=awesome')
            # result = urllib.urlopen('https://api.sentigem.com/external/get-sentiment?api-key=03a678d69796e8a821619eaa38714674ksB7JbwOKhU-5XWofHGa1edqg4AnDzrV&text='+text)
            json_data = json.loads(result.read())
            tweet['label'] = json_data['polarity']
            if json_data['errors'] or json_data['status'] == -1 or json_data['status'] == -2:
                print json_data
            tweets_mixed.append(tweet)


        with open('tweets_data/mixed_train_sentiments.json', 'w') as tweets_sentiments_file:
                json.dump(tweets_mixed, tweets_sentiments_file)


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
        data= urllib.urlencode({'text':text, 'api-key':API_KEY})

        result = urllib.urlopen('https://api.sentigem.com/external/get-sentiment?', data)
        # result = urllib.urlopen('https://api.sentigem.com/external/get-sentiment?api-key=03a678d69796e8a821619eaa38714674ksB7JbwOKhU-5XWofHGa1edqg4AnDzrV&text=awesome')
        # result = urllib.urlopen('https://api.sentigem.com/external/get-sentiment?api-key=03a678d69796e8a821619eaa38714674ksB7JbwOKhU-5XWofHGa1edqg4AnDzrV&text='+text)
        json_data = json.loads(result.read())
        tweet['label'] = json_data['polarity']


    with open('tweets_data/' + tweets_file + '_sentiments.json', 'w') as tweets_sentiments_file:
        if max_tweets != None:
            json.dump(tweets[:max_tweets], tweets_sentiments_file)
        else:
            json.dump(tweets, tweets_sentiments_file)


if __name__ == '__main__':
    sentiment_api_mixed(6000)
    # sentiment_api(handles_lst[0], TWEET_LIMIT)
