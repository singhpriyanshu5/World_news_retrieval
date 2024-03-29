from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from utility import save_as_csv, handles_lst
import json
import nltk
import re
import string
lemmatizer = WordNetLemmatizer()


def get_pos_code(tag):
    if tag == None:
        return ''
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    elif tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    else:
        return ''


def process_apostrophe(word, pos_tag):
    if word == "'ll":
        word = "will"
    elif word == "n't":
        word = "not"
    elif word == "'re":
        word = "are"
    elif word == "'ve":
        word = "have"
    elif word == "'s" and pos_tag == "VBZ":
        word = "is"
    return word

def preprocess_individual(filename):
    # open file

    tweet_text_lst = []
    with open('tweets_data/' + filename + '.json') as json_file:
        tweets = json.load(json_file)
    # load the text of the tweet to a list
    for index, tweet in enumerate(tweets):
        text = tweet['text'].encode('ascii', 'ignore')
        tweet_text_lst.append(text)

    # preprocess
    stop_words = stopwords.words('english')

    # convert to lower case
    processed_data = [sentence.lower() for sentence in tweet_text_lst]

    # remove html
    processed_data = [BeautifulSoup(sentence, "html.parser").get_text() for sentence in processed_data]

    # split sentence to words
    processed_data = [sentence.split() for sentence in processed_data]

    tweets_list = []
    for sentence in processed_data:
        # Remove links
        sentence = [word for word in sentence if not re.match("^http\S+", word)]

        # Remove mention
        sentence = [word for word in sentence if not re.match("\S*@\S+", word)]

        # Remove hashtag
        sentence = [word for word in sentence if not re.match("\S*#\S+", word)]

        tweet_text = " ".join(sentence)
        tweets_list.append(tweet_text)

    for i in xrange(len(tweets_list)):
        tweet = tweets_list[i]
        tokens = word_tokenize(tweet)

        preprocessed_word_lst = []
        for (word,pos_tag) in nltk.pos_tag(tokens):
            word = process_apostrophe(word, pos_tag)

            if word in stop_words:
                continue
            elif pos_tag != None and pos_tag in [".", "TO", "IN", "DT", "UH", "WDT", "WP", "WP$", "WRB"]:
                continue

            pos_code = get_pos_code(pos_tag)

            if pos_code != '':
                word = lemmatizer.lemmatize(word, pos_code)
                preprocessed_word_lst.append(word)

        preprocessed_tweet = " ".join(preprocessed_word_lst)

        preprocessed_tweet = preprocessed_tweet.encode('utf-8').translate(None, string.punctuation)

        tweets_list[i] = preprocessed_tweet
        tweets[i]['ptext'] = preprocessed_tweet



    save_as_csv('tweets_data/'+filename+'_preprocessed.csv', tweets_list)

    with open('tweets_data/'+filename +'_preprocessed.json', 'w') as tf:
        json.dump(tweets, tf)

    # store a list of the labels in a csv file
    label_list = []
    with open('tweets_data/' + filename + '.json') as json_file:
        tweets = json.load(json_file)
        for tweet in tweets:
            label_list.append(tweet['label'])
            save_as_csv('tweets_data/'+filename+'_labels_list.csv', label_list)


def preprocess(handles):
    # open file
    # sentiment_handle = handles[0]
    # handles.insert(0,sentiment_handle+'_sentiments')
    for handle_index,handle in enumerate(handles):

        tweet_text_lst = []
        filename = handle+'_data'
        # filename = handle if handle_index == 0 else handle+'_data'
        with open('tweets_data/' + filename + '.json') as json_file:
            tweets = json.load(json_file)
        # load the text of the tweet to a list
        for index, tweet in enumerate(tweets):
            text = tweet['text'].encode('ascii', 'ignore')
            tweet_text_lst.append(text)

        # preprocess
        stop_words = stopwords.words('english')

        # convert to lower case
        processed_data = [sentence.lower() for sentence in tweet_text_lst]

        # remove html
        processed_data = [BeautifulSoup(sentence, "html.parser").get_text() for sentence in processed_data]

        # split sentence to words
        processed_data = [sentence.split() for sentence in processed_data]

        tweets_list = []
        for sentence in processed_data:
            # Remove links
            sentence = [word for word in sentence if not re.match("^http\S+", word)]

            # Remove mention
            sentence = [word for word in sentence if not re.match("\S*@\S+", word)]

            # Remove hashtag
            sentence = [word for word in sentence if not re.match("\S*#\S+", word)]

            tweet_text = " ".join(sentence)
            tweets_list.append(tweet_text)

        for i in xrange(len(tweets_list)):
            tweet = tweets_list[i]
            tokens = word_tokenize(tweet)

            preprocessed_word_lst = []
            for (word,pos_tag) in nltk.pos_tag(tokens):
                word = process_apostrophe(word, pos_tag)

                if word in stop_words:
                    continue
                elif pos_tag != None and pos_tag in [".", "TO", "IN", "DT", "UH", "WDT", "WP", "WP$", "WRB"]:
                    continue

                pos_code = get_pos_code(pos_tag)

                if pos_code != '':
                    word = lemmatizer.lemmatize(word, pos_code)
                    preprocessed_word_lst.append(word)

            preprocessed_tweet = " ".join(preprocessed_word_lst)

            preprocessed_tweet = preprocessed_tweet.encode('utf-8').translate(None, string.punctuation)

            tweets_list[i] = preprocessed_tweet
            tweets[i]['ptext'] = preprocessed_tweet

        with open('tweets_data/' + filename + '_preprocessed.json', 'w') as tf:
            json.dump(tweets, tf)



if __name__ == '__main__':
    preprocess_individual('mixed_train_sentiments')
    preprocess(handles_lst)
