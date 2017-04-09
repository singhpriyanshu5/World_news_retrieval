from utility import create_directory, save_as_csv
from get_data import get_data
from evaluation_metrics import generate_eval_metrics, class_list, evaluate
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import label_binarize
from sklearn.naive_bayes import GaussianNB

def save_model(model, file_name):

    create_directory('model')
    joblib.dump(model, 'model/%s.pkl' % file_name)


def save_vectorizer(model, file_name):

    create_directory('model')
    joblib.dump(model, 'model/%s.pkl' % file_name)

def nb_classifier():
    label_list = get_data("labels")
    tweet_list = get_data("tweets")
    # vectorise using tf-idf
    vectorizer = TfidfVectorizer(min_df=1,
    max_features=20000,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    ngram_range=(1, 3))

    ## do transformation into vector
    fitted_vectorizer = vectorizer.fit(tweet_list)
    vectorized_tweet_list = fitted_vectorizer.transform(tweet_list)
    train_vector, test_vector, train_labels, test_labels = train_test_split(vectorized_tweet_list,
    label_list,
    test_size=0.2,
    random_state=42)

    print "running naive bayes with training set 80%"

    # train model and predict
    classifier = GaussianNB()
    result = classifier.fit(train_vector.todense(), train_labels)
    prediction = result.predict(test_vector.todense())


    # output result to csv
    create_directory('data')
    save_as_csv("data/nb_test_labels.csv", test_labels)
    prediction.tofile("data/nb_tfidf.csv", sep=',')

    save_model(classifier, 'nb_tfidf')
    save_vectorizer(fitted_vectorizer, 'vectorizer_tfidf')

    # evaluation
    # label_score = classifier.decision_function(test_vector)
    binarized_prediction = label_binarize(prediction, classes=class_list)
    binarized_labels = label_binarize(test_labels, classes=class_list)

    # evaluate(binarized_result, binarized_labels, label_score, 'nb_tfidf')
    generate_eval_metrics(binarized_prediction, 'nb_tfidf', binarized_labels)

if __name__ == "__main__":
    nb_classifier()
