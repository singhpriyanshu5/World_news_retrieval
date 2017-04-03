from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Pool
import classify_main
import json
import tech_crawler
import socket
import threading
import urllib2
import os

def crawl_incremental_data(twitter_handle):
    print "crawling incremental data from "+twitter_handle
    tech_crawler.crawl(twitter_handle)

def update_solr():
    json_file = open('tweets_data/classified_tweets.json')
    python_data_structure = json.load(json_file)
    json_string = json.dumps(python_data_structure)

    try:
        print "Updating solr server"

        req = urllib2.Request(url='http://localhost:8983/solr/tech_news/update/json?commit=true', data=json_string)
        req.add_header('Content-type', 'application/json')
        response = urllib2.urlopen(req)

    except (socket.timeout, urllib2.URLError) as error:
        print error
        raise

def background_process():
    # crawl data
    p = Pool(processes=5)
    res = p.apply_async(crawl_incremental_data, args=('TechCrunch',))
    res = p.apply_async(crawl_incremental_data, args=('mashabletech',))
    res = p.apply_async(crawl_incremental_data, args=('WIRED',))
    res = p.apply_async(crawl_incremental_data, args=('pogue',))
    res = p.apply_async(crawl_incremental_data, args=('e27co',))
    p.close()
    p.join()
    print "Finish crawling"

    # classify data
    classify_main.classify_main()
    print "Finish classifying"

    # update solr server
    update_solr()
    print "Finish updating"

@csrf_exempt
def recrawl(request):
    t = threading.Thread(target=background_process)
    # Want the program to wait on this thread before shutting down.
    t.setDaemon(False)
    t.start()

    return HttpResponse()
