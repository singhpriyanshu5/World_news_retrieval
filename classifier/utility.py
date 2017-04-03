import csv
import os

TWEET_LIMIT = 100

def save_as_csv(file_path, data):
    with open(file_path, 'w') as f:
      wr = csv.writer(f, quoting=csv.QUOTE_ALL)
      wr.writerow(data)

def create_directory(dir):
    try:
        os.makedirs(dir)
    except OSError:
        if not os.path.isdir(dir):
            raise
