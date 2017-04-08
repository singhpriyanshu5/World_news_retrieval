from utility import create_directory
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, precision_recall_curve, average_precision_score, f1_score, precision_score, recall_score
import numpy as np

class_list = ['positive', 'negative', 'neutral']


def evaluate(binarise_result, y_test, y_score, file_name):
  """
  computes the accuracy, precision and recall. plots the precision and recall curve. saves the plots to the figure folder.
  :param binarise_result: list of binarised result after prediction from classifier
  :type binarise_result: list[list[int]]
  :param y_test: list of binarised labels from the test set
  :type y_test: list[list[int]]
  :param y_score: distance of each sample from the decision boundary for each class
  :type y_score:list[list[float]]
  :param file_name: directory name for saving all figures from the plots
  :type file_name: str
  :return:
  :rtype:
  """
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

  # create directory
  create_directory('figure')
  create_directory('figure/' + file_name)

  # plots
  plot_precision_recall_curve(average_precision, precision, recall, file_name)
  # Plot Precision-Recall curve for each class
  plot_precision_recall_curve_all_classes(average_precision, precision, recall, file_name,
                                          num_class)

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


def plot_precision_recall_curve_all_classes(average_precision,
                                            precision,
                                            recall,
                                            file_name,
                                            num_class,
                                            show_plot=False):
  plt.clf()
  plt.plot(recall["micro"],
           precision["micro"],
           label='micro-average Precision-recall curve (area = {0:0.2f})'
           ''.format(average_precision["micro"]))
  for i in range(num_class):
    plt.plot(recall[i],
             precision[i],
             label='Precision-recall curve of class {0} (area = {1:0.2f})'
             ''.format(i, average_precision[i]))
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('Recall')
  plt.ylabel('Precision')
  plt.title('Extension of Precision-Recall curve to multi-class')
  plt.legend(loc="upper left")
  plt.savefig('figure/' + file_name + '/precision_recall_curve_all.png')
  if show_plot:
    plt.show()


def plot_precision_recall_curve(average_precision, precision, recall, file_name, show_plot=False):
  plt.clf()
  plt.plot(recall[0], precision[0], label='Precision-Recall curve')
  plt.xlabel('Recall')
  plt.ylabel('Precision')
  plt.ylim([0.0, 1.05])
  plt.xlim([0.0, 1.0])
  plt.title('Precision-Recall example: AUC={0:0.2f}'.format(average_precision[0]))
  plt.legend(loc="upper left")
  plt.savefig('figure/' + file_name + '/precision_recall_curve.png')
  if show_plot:
    plt.show()
