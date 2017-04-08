from utility import create_directory, save_as_csv
from get_data import get_data
from evaluation_metrics import class_list, generate_eval_metrics
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import label_binarize
from sklearn.externals import joblib

def save_model(model, file_name):
  # create_directory('model')
  # with open('model/%s.pickle' % file_name, 'wb') as f:
  #   cPickle.dump(model, f)
  create_directory('model')
  joblib.dump(model, 'model/%s.pkl' % file_name)

def random_forest_classify():
    labels_list = get_data("labels")
    tweets_list = get_data("tweets")

    vectorizer = TfidfVectorizer(min_df=1,
                               max_features=35000,
                               strip_accents='unicode',
                               analyzer='word',
                               token_pattern=r'\w{1,}',
                               ngram_range=(1, 3),
                               use_idf=1,
                               smooth_idf=1,
                               sublinear_tf=1,)

    vectorizer.fit(tweets_list)
    tweets_vectors = vectorizer.transform(tweets_list)
    train_vector, test_vector, train_labels, test_labels = train_test_split(tweets_vectors,
                                                                          labels_list,
                                                                          test_size=0.2,
                                                                          random_state=42)

    num_estimators = 10
    random_forest_classifier = RandomForestClassifier(n_estimators = num_estimators, n_jobs=4)
    result = random_forest_classifier.fit(train_vector, train_labels)
    prediction = result.predict(test_vector)

    create_directory('data')
    prediction.tofile("data/random_forest_tfidf.csv", sep=',')
    save_as_csv("data/random_forest_test_labels.csv", test_labels)
    save_model(random_forest_classifier, 'rf_tfidf')

    binarized_prediction = label_binarize(prediction, classes=class_list)
    binarized_labels = label_binarize(test_labels, classes=class_list)
    generate_eval_metrics(binarized_prediction, 'random_forest_tfidf', binarized_labels)

if __name__ == "__main__":
    random_forest_classify()
