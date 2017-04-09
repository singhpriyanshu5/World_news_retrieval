# World News Retrieval

CZ4034 Information Retrieval Assignment

## Setting up the Crawler

First, we install all requirements for crawler by using the following command:

```Shell
$ pip install -r crawler/requirements.txt
```

The crawler will crawl [cnnbrk](https://twitter.com/cnnbrk), [FoxNews](https://twitter.com/FoxNews), [BBCWorld](https://twitter.com/BBCWorld), [timesofindia](https://twitter.com/timesofindia), and [STcom](https://twitter.com/STcom) twitter timeline. To use this crawler, we first need to obtain an API key from [Twitter Application Management](https://apps.twitter.com) website. Next, create a file `twitter_app_keys.py` in `crawler` folder. This file will not be checked in to Git.

```Python
# Replace the values with your API key values
CONSUMER_KEY = 'Your key here'
CONSUMER_SECRET = 'Your key here'
ACCESS_TOKEN = 'Your key here'
ACCESS_TOKEN_SECRET = 'Your key here'
```

We run the crawler by using the following command:

```Shell
$ python crawler/news_crawler.py
```

Five json files, `cnnbrk.json`, `FoxNews.json`, `BBCWorld`, `timesofindia`, and `STcom` will be created at the `tweets_data` directory of this project.

To count number of words in crawled data:

```Shell
$ python crawler/word_counter.py
```

## Incremental crawler

First, we install all requirements for the incremental crawler by using the following command:

```Shell
$ pip install -r inc_crawler/requirements.txt
```

The incremental craweler is a Django server and rely on the crawler to do the recrawling task for incremental index. When user submits a request to the server, it will perform an asynchronous task to crawl the tweets and send an update request to Solr server. To run the recrawler server, we first need to setup the crawler, as mentioned in previous section. Then, we run the following commands:

```Shell
$ cd inc_crawler
$ python manage.py migrate
$ python manage.py runserver
```

To test the recrawler, we just need to submit a GET/POST request to `http://localhost:8000/incremental_crawler/recrawl`. The recrawler will return a 200 HTTP reponse immediately and crawling the first 200 tweets from selected accounts asynchronously.



## Classifier

First, we install all requirements for classifier by using the following command:

```Shell
$ pip install -r classifier/requirements.txt
```

You need to run the crawler at least once, and make sure that `_data.json` files for all the twitter handles are available in data folder. The pipeline of our classifier is shown in the figure below:

``` Shell
$ python classifier/sentiment_allocation.py
```

```
 sentiment_allocation.py --> mixed_train_sentiments.py --> preprocess.py --> classifier --> evaluation_metrics.py
```


Next, run `main.py`. It does preprocessing to the data crawled, and runs 3 classifiers next.

```Shell
$ python classifier/main.py
```

The `figure` folder contains the graphs of the precision recall curve. The `metric_result` folder contains the evaluation metrics of the classifier and the timing to run the classifier. The `model` folder contains the trained classifier.

Alternatively, you may run the scripts individually, as shown in the following sections

## Indexing

We start Solr 5.0 server and index our data by using the following commands:

```Shell
$ solr start -s root_of_project/index/solr
$ post -c sport classified_tweets.json
```

### Preprocessing
The preprocessing step will do the following in sequence:

1. lower case
2. remove html
3. remove links
4. remove mention
5. remove hashtag
6. lemmatization and remove stopwords
7. remove punctuation

Then, it will output the preprocessed data to `labelled_tweets.csv` and `label_api.csv`. We can run the preprocess step by using the following script:

```Shell
$ python classifier/preprocess.py
```

Example content of `labelled_tweets.csv`:

```
"buzzer-beating 3 win crucial bubble game make gary payton happy? #pac12afterdark never disappoints. https://t.co/hh0omzffa8","diaz: you're steroids mcgregor: sure am. i'm animal. icymi: #ufc196 presser went expected. https://t.co/jqb72ohv4g"
```

### Classification
After preprocessing step, we will run train some classifiers and evaluate the classifier. Currently, we have three classifier, i.e. linear support vector classification, gensim classifier, and ensemble classifier. By default, the following scripts will use `evaluation_metrics.py` to generate evalutation metrics.

#### Linear support vector classification
output:

- data/tfidf_linsvc.csv

- figure/tfidf_linsvc

- metric_result/tfidf_linsvc.txt

- model/tfidf_linsvc.pkl*

```Shell
$ python classifier/linear_svc.py
```

#### Gensim classifier
output:

- data/w2v_linsvc.csv

- figure/w2v_linsvc

- metric_result/w2v_linsvc.txt

- model/w2v_linsvc.doc2vec

```Shell
$ python classifier/gensim_classifier.py
```

#### Ensemble classifier

output:

- data/tfidf_ada.csv

- metric/tfidf_ada.txt

- model/tfidf_ada.pickle

```Shell
$ python classifier/ensemble_classifier.py
```

#### Inter annotator agreement
The preprocessing.py class calls the nltk [annotation task](https://github.com/tousif/nltk-gae/blob/master/nltk/metrics/agreement.py).

### Classify all crawled data

```Shell
$ python classifier/classifier_data.py

## UI Client

We have a simple user interface that use Solr server to retrieve sport news. Current UI version has two functions:

- A button to trigger the crawling in the backend
- A text area waiting for keywords. The click of search button will trigger a query to backend solr to retrieve records. Then records are displayed in the page.

To install all components for this website, we first need to install bower using [node package manager](https://www.npmjs.com/):

```Shell
$ npm install -g bower
```

Then we install all dependencies using bower:

```Shell
$ cd UI
$ bower install
```

You can open the `UI/index.html` file to view the simple website. Please take note that some functionality may not work if you didn't run Solr server and serve static content from the same domain.


```
