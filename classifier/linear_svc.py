from utility import create_directory, save_as_csv
# from get_data import get_data
from evaluation_metrics import evaluate, class_list, generate_eval_metrics
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import get_data

def save_model(model, file_name):
    create_directory('model')
    joblib.dump(model, 'model/%s.pkl' % file_name)


def save_vectorizer(model, file_name):
    create_directory('model')
    joblib.dump(model, 'model/%s.pkl' % file_name)

def linear_svc():
    label_list = get_data.get_data("labels")
    tweet_list = get_data.get_data("tweets")
    # vectorise using tf-idf
    vectorizer = TfidfVectorizer(min_df=1,
    max_features=35000,
    stop_words='english',
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    ngram_range=(1, 3))

    ## do transformation into vector
    fitted_vectorizer = vectorizer.fit(tweet_list)
    vectorized_tweet_list = fitted_vectorizer.transform(tweet_list)

    # pca = PCA(n_components=2).fit(vectorized_tweet_list.todense())
    # data2D = pca.transform(vectorized_tweet_list.todense())
    # plt.scatter(data2D[:,0], data2D[:,1], c='red')
    # plt.show()

    train_vector, test_vector, train_labels, test_labels = train_test_split(vectorized_tweet_list,
    label_list,
    test_size=0.2,
    random_state=42)

    # print train_vector.todense().shape
    # print test_vector.todense().shape
    # print len(label_list)

    dense_train = train_vector.todense()
    pos_vectors = []
    neg_vectors = []
    neutral_vectors = []
    # for i in xrange(dense_train.shape[0]):
    #     if label_list[i] == "positive":
    #         # pos_vectors = np.append(pos_vectors, dense_train[i], axis=0)
    #         pos_vectors.extend(dense_train[i][0,:])
    #     elif label_list[i] == "negative":
    #         neg_vectors.extend(dense_train[i][0,:])
    #     elif label_list[i] == "neutral":
    #         neutral_vectors.extend(dense_train[i][0,:])
    # pos_vectors = np.array(pos_vectors)
    # neg_vectors = np.array(neg_vectors)
    # neutral_vectors = np.array(neutral_vectors)
    #
    # pca_pos = PCA(n_components=2).fit(pos_vectors[:,0,:])
    # data_pos = pca_pos.transform(pos_vectors[:,0,:])
    #
    # pca_neg = PCA(n_components=2).fit(neg_vectors[:,0,:])
    # data_neg = pca_neg.transform(neg_vectors[:,0,:])
    #
    # pca_neutral = PCA(n_components=2).fit(neutral_vectors[:,0,:])
    # data_neutral = pca_neutral.transform(neutral_vectors[:,0,:])
    #
    # # pca_test = PCA(n_components=2).fit(test_vector.todense())
    # # data_test = pca_test.transform(test_vector.todense())
    #
    # plt.scatter(data_pos[:,0], data_pos[:,1], c='blue')
    # plt.scatter(data_neg[:,0], data_neg[:,1], c='red')
    # plt.scatter(data_neutral[:,0], data_neutral[:,1], c='green')
    # # plt.scatter(data_test[:,0], data_test[:,1], c='yellow')
    # plt.show()

    # pca_train = PCA(n_components=10000).fit(train_vector.todense())
    # data_train = pca_train.transform(train_vector.todense())
    # data_test = pca_train.transform(test_vector.todense())


    # train model and predict
    model = LinearSVC()
    ovr_classifier = OneVsRestClassifier(model).fit(train_vector, train_labels)
    prediction = ovr_classifier.predict(test_vector)

    # ovr_classifier = OneVsRestClassifier(model).fit(data_train, train_labels)
    # prediction = ovr_classifier.predict(data_test)
    # prediction = ovr_classifier.predict(train_vector)

    confusion_matrix = {}
    predicted_positive = {'actual_positive':0, 'actual_negative':0, 'actual_neutral':0}
    predicted_negative = {'actual_positive':0, 'actual_negative':0, 'actual_neutral':0}
    predicted_neutral = {'actual_positive':0, 'actual_negative':0, 'actual_neutral':0}

    for label_index, label in enumerate(prediction):

        if label == "positive":
            if test_labels[label_index] == "positive":
                predicted_positive['actual_positive'] += 1
            elif test_labels[label_index] == "negative":
                predicted_positive['actual_negative'] += 1
            elif test_labels[label_index] == "neutral":
                predicted_positive['actual_neutral'] += 1
        elif label == "negative":
            if test_labels[label_index] == "positive":
                predicted_negative['actual_positive'] += 1
            elif test_labels[label_index] == "negative":
                predicted_negative['actual_negative'] += 1
            elif test_labels[label_index] == "neutral":
                predicted_negative['actual_neutral'] += 1
        if label == "neutral":
            if test_labels[label_index] == "positive":
                predicted_neutral['actual_positive'] += 1
            elif test_labels[label_index] == "negative":
                predicted_neutral['actual_negative'] += 1
            elif test_labels[label_index] == "neutral":
                predicted_neutral['actual_neutral'] += 1

    # for label_index, label in enumerate(prediction):
    #
    #     if label == "positive":
    #         if train_labels[label_index] == "positive":
    #             predicted_positive['actual_positive'] += 1
    #         elif train_labels[label_index] == "negative":
    #             predicted_positive['actual_negative'] += 1
    #         elif train_labels[label_index] == "neutral":
    #             predicted_positive['actual_neutral'] += 1
    #     elif label == "negative":
    #         if train_labels[label_index] == "positive":
    #             predicted_negative['actual_positive'] += 1
    #         elif train_labels[label_index] == "negative":
    #             predicted_negative['actual_negative'] += 1
    #         elif train_labels[label_index] == "neutral":
    #             predicted_negative['actual_neutral'] += 1
    #     if label == "neutral":
    #         if train_labels[label_index] == "positive":
    #             predicted_neutral['actual_positive'] += 1
    #         elif train_labels[label_index] == "negative":
    #             predicted_neutral['actual_negative'] += 1
    #         elif train_labels[label_index] == "neutral":
    #             predicted_neutral['actual_neutral'] += 1

    confusion_matrix['predicted_positive'] = predicted_positive
    confusion_matrix['predicted_negative'] = predicted_negative
    confusion_matrix['predicted_neutral'] = predicted_neutral

    print confusion_matrix



    # output result to csv
    create_directory('data')
    save_as_csv("data/linearsvc_test_labels.csv", test_labels)
    prediction.tofile("data/linearsvc_tfidf.csv", sep=',')

    save_model(ovr_classifier, 'linearsvc_tfidf')
    save_vectorizer(fitted_vectorizer, 'vectorizer_tfidf')

    # evaluation
    # label_score = ovr_classifier.decision_function(test_vector)
    label_score = ovr_classifier.decision_function(test_vector)
    binarized_prediction = label_binarize(prediction, classes=class_list)
    binarized_labels = label_binarize(test_labels, classes=class_list)
    evaluate(binarized_prediction, binarized_labels, label_score, 'linearsvc_tfidf')

    # train_score = ovr_classifier.decision_function(train_vector)
    # binarized_prediction = label_binarize(prediction, classes=class_list)
    # binarized_labels = label_binarize(train_labels, classes=class_list)
    # evaluate(binarized_prediction, binarized_labels, train_score, 'linearsvc_tfidf_train')


    # generate_eval_metrics(binarized_prediction, 'linsvc_tfidf', binarized_labels)

if __name__ == "__main__":
    linear_svc()
