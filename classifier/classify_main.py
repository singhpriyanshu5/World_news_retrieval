from sklearn.externals import joblib
import json

filenames = ['TechCrunch', 'mashabletech', 'pogue', 'e27co', 'WIRED']
ALL_DATA_FILE_PATH = 'data/classified_tweets.json'

def classify_main():
    model = joblib.load('model/linearsvc_tfidf.pkl')
    vectorizer = joblib.load('model/vectorizer_tfidf.pkl')

    all_tweets_json = []
    all_tweets_text = []
    for filename in filenames:
        with open('tweets_data/'+filename+'_data.json') as json_file:
            tweets_json = json.load(json_file)
            tweets_text = [tweet['text'] for tweet in tweets_json]
            all_tweets_json.extend(tweets_json)
            all_tweets_text.extend(tweets_text)

    vectorized_tweets = vectorizer.transform(all_tweets_text)
    prediction = model.predict(vectorized_tweets)

    for tweet_json, label in zip(all_tweets_json, prediction):
        tweet_json['label'] = label

    with open('tweets_data/classified_tweets.json', 'w') as f:
        json.dump(all_tweets_json, f)

if __name__ == "__main__":
    classify_main()
