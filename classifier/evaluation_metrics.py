from utility import create_directory
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, precision_recall_curve, average_precision_score, f1_score, precision_score, recall_score
import numpy as np

class_list = ['positive', 'negative', 'neutral']


def evaluate(binarise_result, y_test, y_score, file_name):

  num_class = y_test.shape[1]

  # Compute Precision-Recall and plot curve
  precision = dict()
  recall = dict()
  average_precision = dict()
  for i in range(num_class):
    precision[i], recall[i], _ = precision_recall_curve(y_test[:, i], y_score[:, i])
    average_precision[i] = average_precision_score(y_test[:, i], y_score[:, i])

  # Compute micro-average ROC curve and ROC area
  precision["micro"], recall["micro"], _ = precision_recall_curve(y_test.ravel(), y_score.ravel())
  average_precision["micro"] = average_precision_score(y_test, y_score, average="micro")

  generate_eval_metrics(binarise_result, file_name, y_test)


def generate_eval_metrics(binarise_result, file_name, y_test):
  accuracy = accuracy_score(np.array(y_test), np.array(binarise_result))
  precision_macro = precision_score(y_test, binarise_result, average="macro")
  recall_macro = recall_score(y_test, binarise_result, average="macro")
  f1_measure_macro = f1_score(y_test, binarise_result, average="macro")
  precision_weighted= precision_score(y_test, binarise_result, average="weighted")

  precision_micro = precision_score(y_test, binarise_result, average="micro")
  recall_micro = recall_score(y_test, binarise_result, average="micro")
  f1_measure_micro = f1_score(y_test, binarise_result, average="micro")

  # save results in a txt file
  create_directory('metric_result')
  with open("metric_result/" + file_name + ".txt", "w") as text_file:
    text_file.write("Accuracy: {0}\n".format(accuracy))
    text_file.write("Precision(Macro): {0}\n".format(precision_macro))
    text_file.write("Recall(Macro): {0}\n".format(recall_macro))
    text_file.write("F1 measure(Macro): {0}\n\n".format(f1_measure_macro))
    text_file.write("Precision(Weighted): {0}\n\n".format(precision_weighted))

    text_file.write("Precision(Micro): {0}\n".format(precision_micro))
    text_file.write("Recall(Micro): {0}\n".format(recall_micro))
    text_file.write("F1 measure(Micro): {0}\n".format(f1_measure_micro))
