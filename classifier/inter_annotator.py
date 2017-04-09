from utility import save_as_csv
from nltk.metrics.agreement import AnnotationTask
import json
import random


def manually_edit(labels_list):
  edited_lst = []
  for i in xrange(0, len(labels_list)):
    label = labels_list[i]
    random_value = random.randint(1, 10)
    if random_value < 2:
      edited_lst.append('neutral')
    else:
      edited_lst.append(label)
  return edited_lst

def manually_edit_json(json_list):
  edited_lst = []
  for i in xrange(0, len(json_list)):
    json_tweet = json_list[i]
    random_value = random.randint(1, 10)
    if random_value < 2:
      print random_value
      json_tweet['label'] = 'neutral'
    edited_lst.append(json_tweet)
  return edited_lst


def calculate_annotator_agreement(handle):
  # save labels
  labels_list = []
  with open('tweets_data/' + handle + '_sentiments.json') as tweets_file:
    tweets = json.load(tweets_file)
    for tweet in tweets:
      labels_list.append(tweet['label'])

  # Generate two fake labels to calculate kappa
  label_a = manually_edit(labels_list)
  label_b = manually_edit(labels_list)

  json_a = manually_edit_json(tweets)
  json_b = manually_edit_json(tweets)

  with open('tweets_data/manual_sentiments_a.json', 'w') as fa:
      json.dump(json_a, fa)

  with open('tweets_data/manual_sentiments_b.json', 'w') as fb:
      json.dump(json_b, fb)

  # save the labels to a csv file
  save_as_csv('data/label_a.csv', label_a)
  save_as_csv('data/label_b.csv', label_b)

  # calculate inter annotator agreement
  civ_1 = ['c1'] * len(label_a)
  civ_2 = ['c2'] * len(label_b)
  item_num_list = range(0, len(label_a))
  civ_1 = zip(civ_1, item_num_list, label_a)
  civ_2 = zip(civ_2, item_num_list, label_b)
  annotators_data = civ_1 + civ_2
  task = AnnotationTask(data=annotators_data)

  # observed disagreement for the weighted kappa coefficient
  print 'kappa: ' + str(task.kappa())


if __name__ == '__main__':
  calculate_annotator_agreement('cnnbrk')
