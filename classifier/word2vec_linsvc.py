from utility import create_directory
from get_data import get_data, train_test_split
from evaluation_metrics import evaluate, class_list
from gensim.models.word2vec import Word2Vec
from sklearn.externals import joblib
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.svm import LinearSVC
from sklearn.preprocessing import Imputer
import logging
import numpy as np


def get_feature_vector(word_list, w2v_model, num_features):
    """
    Averages the word vectors for a sentence
    """
    feature_vector = np.zeros((num_features,), dtype="float32")
    index2word_set = set(w2v_model.index2word)
    # check if in model's vocab, add vector to total
    num_words = 0
    for word in word_list:
        if word in index2word_set:
            num_words = num_words + 1.
            feature_vector = np.add(feature_vector, w2v_model[word])

    # Divide the result by the number of words to get the average
    feature_vector = np.divide(feature_vector, num_words)
    return feature_vector

def get_avg_feature_vector(sentences_list, w2v_model, num_features):

    avg_vector_list = np.zeros((len(sentences_list), num_features), dtype = "float32")
    i = 0
    for sentence in sentences_list:
        if i % 50.0 == 0:
            print "Sentence number %d of %d" % (i, len(sentences_list))
        avg_vector_list[i] = get_feature_vector(sentence, w2v_model, num_features)
        i = i + 1
    return avg_vector_list

def linearsvc_w2v_classify():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    labels_list = get_data("labels")
    tweets_list = get_data("tweets")

    sentences_list = []
    for tweet in tweets_list:
        sentences_list.append(tweet.split())

    num_features = 100
    w2v_model = Word2Vec(sentences_list, workers = 4, \
              size = num_features, min_count = 1, \
              window = 2, sample = 1e-3, seed=1)

    ## @TODO: try to use the train_test_split provided by sklearn
    index_value, train_set, test_set = train_test_split(0.80, sentences_list)

    train_vector = get_avg_feature_vector(train_set, w2v_model, num_features)
    test_vector = get_avg_feature_vector(test_set, w2v_model, num_features)

    train_vector = Imputer().fit_transform(train_vector)
    test_vector = Imputer().fit_transform(test_vector)

    model = LinearSVC()
    classifier = OneVsRestClassifier(model).fit(train_vector, labels_list[:index_value])
    prediction = classifier.predict(test_vector)

    create_directory('data')
    prediction.tofile("data/linearsvc_w2v.csv", sep=',')

    create_directory('model')
    joblib.dump(model, 'model/%s.pkl' % 'linearsvc_w2v')

    test_set_score = classifier.decision_function(test_vector)
    binarize_prediction = label_binarize(prediction, classes=class_list)
    binarize_labels = label_binarize(labels_list, classes=class_list)

    evaluate(binarize_prediction, binarize_labels[index_value:], test_set_score, 'linearsvc_w2v')

if __name__ == "__main__":
    linearsvc_w2v_classify()
