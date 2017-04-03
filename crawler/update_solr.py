import json
import urllib2
import socket

def update_solr(filename):
  json_data = open('tweets_data/'+filename+'_data.json')
  temp = json.load(json_data)
  result_json = json.dumps(temp)

  # send json file to SOLR server
  try:
    print 'updating solr server'

    # You may change solr-node to localhost for development purpose. However, please do not check
    # that in, and keep the base url as solr-node:8983
    req = urllib2.Request(url='http://localhost:8983/solr/tech_news/update/json?commit=true',
                          data=result_json)
    req.add_header('Content-type', 'application/json')
    response = urllib2.urlopen(req)
    print response
  except (socket.timeout, urllib2.URLError) as error:
    print error
    raise

if __name__ == "__main__":
    update_solr('WIRED')
    update_solr('mashabletech')
    update_solr('pogue')
    update_solr('e27co')
