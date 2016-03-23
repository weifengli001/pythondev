# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: BSD 3 clause

from __future__ import print_function

from time import time
import sys
import os
import numpy as np
import scipy.sparse as sp
import pylab as pl

from sklearn.datasets import load_mlcomp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cross_validation


print(__doc__)




from sklearn import svm, datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
from sklearn import metrics
from sklearn.svm import LinearSVC, SVC
from utils.helper import read_csv_file
from utils.helper import make_data
import utils

vectorizer = TfidfVectorizer(min_df=1)
def create_tfidf_training_data(docs):
    # Create the training data class labels
    y = [d[1] for d in docs]
    # Create the document corpus list
    corpus = [d[0] for d in docs]
    # Create the TF-IDF vectoriser and transform the corpus
    X = vectorizer.fit_transform(corpus)
    return X, y

def execute_prediction(classif):
    for filename in os.listdir(utils.helper.raw_data_file_path):
        if not filename.endswith('.csv'):
            continue
        filename = utils.helper.raw_data_file_path + '/' + filename
        #out_filename = filename[:-4]
        out_filename = 'prediction'
        out_file = csv.writer(open(out_filename + "_result.csv", "w+"))
        with open(filename) as f:
            myreader = csv.reader(f, delimiter=',')
            for row in myreader:
                print(row)
                X1 = vectorizer.transform([row[2]])
                row.append(classif.predict(X1)[0])
                print(row)
                out_file.writerow(row)




sentiments, texts = read_csv_file(utils.helper.training_file, 5, 15)
data = make_data(texts, sentiments)
X, y = create_tfidf_training_data(data)

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


target_names = ['Positive', 'Neutural', 'Negtive']


###############################################################################
def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Benchmark classifiers
def benchmark(clf_class, params, name):
    print("parameters:", params)
    t0 = time()
    clf = clf_class(**params).fit(X_train, y_train)
    print("done in %fs" % (time() - t0))
    t0 = time()
    pred = clf.predict(X_test)
    print("done in %fs" % (time() - t0))
    #execute_prediction(clf)
    print(clf.score(X_test, y_test))
    predicted = cross_validation.cross_val_predict(clf, X,
                                                y, cv=10)
    score = metrics.accuracy_score(y, predicted)
    print(score)

    print("Classification report on test set for classifier:")
    print(clf)
    print()
    print(classification_report(y_test, pred,
                                target_names=target_names))

    cm = confusion_matrix(y_test, pred)
    print("Confusion matrix:")
    print(cm)

    # Show confusion matrix
    #pl.matshow(cm)
    #pl.title('Confusion matrix of the %s classifier' % name)
    #pl.colorbar()

    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization')
    plt.figure()
    plot_confusion_matrix(cm)


print("Testbenching a MultinomialNB classifier...")
parameters = {'alpha': 0.01}
benchmark(MultinomialNB, parameters, 'MultinomialNB')

print("Testbenching a LinearSVC classifier...")
parameters = {}
benchmark(LinearSVC, parameters, 'LinearSVC')

print("Testbenching a SVC(kernel:rbf) classifier...")
parameters = {
    'C': 10.0,
    'gamma': 0.10000000000000001,
    'kernel': 'rbf'
}
benchmark(SVC, parameters, 'SVC')

print("Testbenching a SVC(kernel:linear) classifier...")
parameters = {
    'C': 1.0,
    'kernel': 'linear'
}
benchmark(SVC, parameters, 'SVC')

pl.show()