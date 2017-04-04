from utility import create_directory, save_as_csv
from get_data import get_data
from evaluation_metrics import evaluate, class_list
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import label_binarize
from sklearn.svm import LinearSVC

def save_model(model, file_name):
    create_directory('model')
    joblib.dump(model, 'model/%s.pkl' % file_name)


def save_vectorizer(model, file_name):
    create_directory('model')
    joblib.dump(model, 'model/%s.pkl' % file_name)

def linear_svc():
    label_list = get_data("labels")
    tweet_list = get_data("tweets")
    # vectorise using tf-idf
    vectorizer = TfidfVectorizer(min_df=3,
    max_features=None,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    ngram_range=(1, 2),
    use_idf=1,
    smooth_idf=1,
    sublinear_tf=1,)

    ## do transformation into vector
    fitted_vectorizer = vectorizer.fit(tweet_list)
    vectorized_tweet_list = fitted_vectorizer.transform(tweet_list)
    train_vector, test_vector, train_labels, test_labels = train_test_split(vectorized_tweet_list,
    label_list,
    test_size=0.8,
    random_state=42)

    # train model and predict
    model = LinearSVC()
    ovr_classifier = OneVsRestClassifier(model).fit(train_vector, train_labels)
    prediction = ovr_classifier.predict(test_vector)

    # output result to csv
    create_directory('data')
    save_as_csv("data/linearsvc_test_labels.csv", test_labels)
    prediction.tofile("data/linearsvc_tfidf.csv", sep=',')

    save_model(ovr_classifier, 'linearsvc_tfidf')
    save_vectorizer(fitted_vectorizer, 'vectorizer_tfidf')

    # evaluation
    label_score = ovr_classifier.decision_function(test_vector)
    binarized_prediction = label_binarize(prediction, classes=class_list)
    binarized_labels = label_binarize(test_labels, classes=class_list)

    evaluate(binarized_prediction, binarized_labels, label_score, 'linearsvc_tfidf')

if __name__ == "__main__":
    linear_svc()
