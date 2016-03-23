
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
                row[2] = row[2].encode('utf-8', 'ignore')
                X1 = vectorizer.transform([row[2]])
                row.append(classif.predict(X1)[0])
                out_file.writerow(row)



sentiments, texts = read_csv_file(utils.helper.training_file, 5, 15)
data = make_data(texts, sentiments)
X, y = create_tfidf_training_data(data)

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)



###############################################################################

#entrance
def main(clf_class, params, name):
    print("parameters:", params)
    t0 = time()
    clf = clf_class(**params).fit(X_train, y_train)
    print("done in %fs" % (time() - t0))
    execute_prediction(clf)


if __name__ == "__main__":
    print("Testbenching a LinearSVC classifier...")
    parameters = {}
    t0 = time()
    main(LinearSVC, parameters, 'LinearSVC')
    print("prediction done in %fs" % (time() - t0))

