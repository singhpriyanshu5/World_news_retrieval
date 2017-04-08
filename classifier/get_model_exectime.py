import timeit
from get_data import get_data
from utility import create_directory



## calculate the average time for classifying the entire dataset
def get_dataset_time(total_time, num_reps):
    return total_time/num_reps

## calculate the average time for classifying each tweet
def get_datapoint_time(dataset_time, num_tweets):
    return dataset_time/num_tweets

def calculate_exectime():
    tweets_list = get_data("tweets")
    num_tweets = len(tweets_list)

    ## setup statement for the linear svc classifier

    linsvc_setup ="""from get_data import get_data;from sklearn.externals import joblib;tweets_list = get_data("tweets");vectorizer = joblib.load('model/vectorizer_tfidf.pkl');vectorized_tweets = vectorizer.transform(tweets_list);linear_svc_model = joblib.load('model/linearsvc_tfidf.pkl');linear_svc_model.predict(vectorized_tweets);
      """
    linsvc_statement = "linear_svc_model.predict(vectorized_tweets)"
    num_reps = 100

    linsvc_time = timeit.timeit(stmt=linsvc_statement, setup=linsvc_setup, number=num_reps)
    linsvc_dataset_time = get_dataset_time(linsvc_time, num_reps)
    linsvc_datapoint_time = get_datapoint_time(linsvc_dataset_time, num_tweets)

    rf_setup = """import cPickle;from get_data import get_data;from sklearn.externals import joblib;tweets_list = get_data("tweets");vectorizer = joblib.load('model/vectorizer_tfidf.pkl');vectorized_tweets = vectorizer.transform(tweets_list); rf_model = joblib.load('model/rf_tfidf.pkl');rf_model.predict(vectorized_tweets);
      """
    rf_statement = "rf_model.predict(vectorized_tweets)"

    rf_time = timeit.timeit(stmt=rf_statement, setup=rf_setup, number=num_reps)
    rf_dataset_time = get_dataset_time(rf_time, num_reps)
    rf_datapoint_time = get_datapoint_time(rf_dataset_time, num_reps)

    create_directory('metric_result')
    with open("metric_result/" + 'timings' + ".txt", "w") as text_file:
        text_file.write("Number of records in dataset: {0}\n".format(num_tweets))
        text_file.write("Linear SVC dataset time: {0}\n".format(linsvc_dataset_time))
        text_file.write("Linear SVC datapoint time: {0}\n".format(linsvc_datapoint_time))
        text_file.write("Random Forest dataset time: {0}\n".format(rf_dataset_time))
        text_file.write("Random Forest datapoint time: {0}\n".format(rf_datapoint_time))

if __name__ == "__main__":
    calculate_exectime()
