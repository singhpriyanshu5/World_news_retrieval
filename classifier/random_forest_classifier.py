from utility import create_directory
from get_data import get_data
from evaluation_metrics import class_list, generate_eval_metrics
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import label_binarize
import cPickle

def save_model(model, file_name):
  create_directory('model')
  with open('model/%s.pickle' % file_name, 'wb') as f:
    cPickle.dump(model, f)

def random_forest_classify():
    labels_list = get_data("labels")
    tweets_list = get_data("tweets")

    vectorizer = TfidfVectorizer(min_df=3,
                               max_features=None,
                               strip_accents='unicode',
                               analyzer='word',
                               token_pattern=r'\w{1,}',
                               ngram_range=(1, 2),
                               use_idf=1,
                               smooth_idf=1,
                               sublinear_tf=1,)

    vectorizer.fit(tweets_list)
    tweets_vectors = vectorizer.transform(tweets_list)
    train_vector, test_vector, train_labels, test_labels = train_test_split(tweets_vectors,
                                                                          labels_list,
                                                                          test_size=0.8,
                                                                          random_state=42)

    num_estimators = 10
    random_forest_classifier = RandomForestClassifier(n_estimators = num_estimators)
    result = random_forest_classifier.fit(train_vector, train_labels)
    prediction = result.predict(test_vector)

    create_directory('data')
    prediction.tofile("data/random_forest_tfidf.csv", sep=',')
    save_model(random_forest_classifier, 'random_forest_tfidf')

    binarized_prediction = label_binarize(prediction, classes=class_list)
    binarized_labels = label_binarize(test_labels, classes=class_list)
    generate_eval_metrics(binarized_prediction, 'random_forest_tfidf', binarized_labels)

if __name__ == "__main__":
    random_forest_classify()
