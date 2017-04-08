import json

###############

handles_lst = ['cnnbrk','BBCWorld', 'FoxNews', 'timesofindia', 'STcom']

###############


def count():
    num_words = 0
    num_tweets = 0
    all_sentences = []
    all_words = []
    for filename in handles_lst:
        with open('tweets_data/'+filename+'_data_preprocessed.json') as json_file:
            tweets_json = json.load(json_file)
            num_words += sum([len(tweet['text'].split()) for tweet in tweets_json])
            for tweet in tweets_json:
                all_sentences.append(tweet['text'])
                all_words.extend(tweet['text'].split())
    print "total number of tweets: {}".format(len(all_sentences))
    print "total number of words: {}".format(len(all_words))
    print "number of unique words: {}".format(len(set(all_words)))

    #         all_sentences.extend(processed_file.split(","))
    #
    # for sentence in all_sentences:
    #     all_words.append(sentence.split())
    # print "total number of tweets: {}".format(len(all_sentences))
    # print "total number of words: {}".format(len(all_words))
    # print "number of unique words: {}".format(len(set(all_words)))

    #         tweets_json = json.load(json_file)
    #         num_words += sum([len(tweet['text'].split()) for tweet in tweets_json])
    #         for tweet in tweets_json:
    #             all_words.add(tweet['text'])
    #         num_tweets += len(tweets_json)
    #
    # print num_words


if __name__ == "__main__":
    count()
