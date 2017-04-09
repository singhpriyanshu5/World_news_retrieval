# World News Retrieval

CZ4034 Information Retrieval Assignment

## Setting up the Crawler

Install all requirements for crawler by using the following command:

```Shell
$ pip install -r crawler/requirements.txt
```

The crawler will crawl [cnnbrk](https://twitter.com/cnnbrk), [FoxNews](https://twitter.com/FoxNews), [BBCWorld](https://twitter.com/BBCWorld), [timesofindia](https://twitter.com/timesofindia), and [STcom](https://twitter.com/STcom) twitter timeline. To use this crawler, first need to obtain API key from [Twitter Application Management](https://apps.twitter.com) website. Then, create a file `twitter_app_keys.py` in the `crawler` folder.

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

Five json files, `cnnbrk.json`, `FoxNews.json`, `BBCWorld`, `timesofindia`, and `STcom` will be created in the `tweets_data` directory of this project.


## Classifier

First, we install all requirements for classifier by using the following command:



You need to run the crawler at least once, and make sure that `_data.json` files for all the twitter handles are available in data folder. The pipeline of our classifier is shown in the figure below:

``` Shell
$ python classifier/sentiment_allocation.py
```

```
 sentiment_allocation.py --> mixed_train_sentiments.json --> preprocess.py --> mixed_train_sentiments_preprocessed.json --> random_forest.py -> classified_tweets.json -> update index using solr
```
``` Shell
$ python classifier/preprocessing_data.py
```
``` Shell
$ python classifier/random_forest_classifier.py
```

In order to classify the all the other tweets, we run the following command. classify_main.py uses the already trained random_forest_classifier (as shown in the previous step) to train the other already preprocessed tweets
``` Shell
$ python classifier/classify_main.py
```

## Indexing

Start the solr server using the following commands:

```Shell
$ solr start -s root_of_project/index/solr
$ post -c world_news classified_tweets.json
```

### Preprocessing
The preprocessing step will do the following in sequence:

1. lower case
2. remove html tags
3. remove hashtags, mentions and links
4. stop words
5. remove contractions(apostrophes)
6. lemmatization
7. remove punctuation

The preprocessed tweets will be stored in `mixed_train_sentiments_preprocessed.json`, the preprocessed text are stored in `mixed_train_sentiments_preprocessed.csv`, `mixed_train_sentiments_preprocessed.csv`



```Shell
$ python classifier/preprocessing_data.py
```

## Incremental crawler

First, we install all requirements for the incremental crawler by using the following command:

```Shell
$ pip install -r inc_crawler/requirements.txt
```

The incremental craweler is a Django server and relies on the crawler for the incremental crawling task. As soon as the user clicks on the crawl button, a get post request with the selected handles is sent to the django server, which crawls the tweets asynchronously, then preprocesses the new tweets, then classifies the new tweets using the random forest classifier and finally updates the index using solr.

```Shell
$ pip install -r classifier/requirements.txt
```

```Shell
$ cd inc_crawler
$ python manage.py migrate
$ python manage.py runserver
```



```

### Classification
After preprocessing step, we will run train some classifiers and evaluate the classifier. Currently, we have three classifier, i.e. linear support vector classification, gensim classifier, and ensemble classifier. By default, the following scripts will use `evaluation_metrics.py` to generate evalutation metrics.



## UI Client

The UI uses a nodejs server for the frontend server and angularJS for the frontend framework.

Install bower using [node package manager](https://www.npmjs.com/):

```Shell
$ npm install -g bower
```

Install all dependencies using bower:

```Shell
$ cd UI
$ bower install
```

Use the `UI/index.html` file to open the home page of our information retrieval system.

```
