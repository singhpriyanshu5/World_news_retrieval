import csv
import os
from utility import TWEET_LIMIT

def get_data(data_type):
    if data_type == "labels":
        with open('tweets_data/sentiment_labels_list.csv', 'r') as labels_file:
            reader = csv.reader(labels_file)
            labels_list = list(reader)[0]
            return labels_list
    elif data_type == "tweets":
        with open('tweets_data/preprocessed_tweets.csv', 'r') as labels_file:
            reader = csv.reader(labels_file)
            tweets_list = list(reader)[0]
            if TWEET_LIMIT != None:
                return tweets_list[:TWEET_LIMIT]
            else:
                return tweets_list

def train_test_split(percentage, data_set):
    # split data into training and test set
    index_value = int(len(data_set) * percentage)
    train_vector = data_set[:index_value]
    test_vector = data_set[index_value:]

    return index_value, train_vector, test_vector
