from __future__ import absolute_import
import sys
import os
from inc_crawler import settings
sys.path.append(os.path.abspath(settings.FILES_DIR))
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from multiprocessing import Pool
from classifier import classify_main, utility, preprocessing_data
import json
from crawler import news_crawler
import socket
import threading
import urllib2




def crawl_incremental_data(twitter_handle):
    print "crawling incremental data from "+twitter_handle
    news_crawler.crawl(twitter_handle)

def update_solr():
    json_file = open('tweets_data/classified_tweets.json')
    python_data_structure = json.load(json_file)
    json_string = json.dumps(python_data_structure)

    try:
        print "Updating solr server"

        req = urllib2.Request(url='http://localhost:8983/solr/world_news/update/json?commit=true', data=json_string)
        req.add_header('Content-type', 'application/json')
        response = urllib2.urlopen(req)

    except (socket.timeout, urllib2.URLError) as error:
        print error
        raise

def main_recrawl(handles_lst):
    # crawl data
    p = Pool(processes=5)
    for handle in handles_lst:
        res = p.apply_async(crawl_incremental_data, args=(handle,))
    p.close()
    p.join()
    print "crawling finished"

    preprocessing_data.preprocess(handles_lst)
    print "preprocessing of the crawled data finished"

    # classify data
    classify_main.classify_main()
    print "classification finished"

    # update solr server
    update_solr()
    print "solr update finished"

@csrf_exempt
def recrawl(request):
    handles_lst = []
    if "handles" in request.GET:
        print "got twitter handles"
        print request.GET['handles']
        if request.GET['handles'] != '':
            handles_lst = (request.GET['handles']).split(',')
        else:
            handles_lst = utility.handles_lst
    main_recrawl(handles_lst)
    if "callback" in request.GET:
        response_json = "{'crawling_done':'true'}"
        data = '%s(%s);' % (request.GET['callback'], response_json)
        return HttpResponse(data, "text/javascript")
    else:
        return HttpResponse('okayy')
