print(__doc__)

import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import csv

vectorizer = TfidfVectorizer(min_df=1)
def create_tfidf_training_data(docs):
    # Create the training data class labels
    y = [d[1] for d in docs]

    # Create the document corpus list
    corpus = [d[0] for d in docs]

    # Create the TF-IDF vectoriser and transform the corpus

    X = vectorizer.fit_transform(corpus)
    return X, y

def train_svm(X, y):
    #clf = SVC(C=1000000.0, gamma=0.10000000000000001, kernel='rbf')
    clf = svm.LinearSVC()
    clf.fit(X, y)
    return clf
def read_csv_file(filename, delimiter = ','):
    ids = []
    values =[]
    with open(filename) as csvfile:
        myreader = csv.reader(csvfile,delimiter=delimiter)
        for row in myreader:
            sentiments.append(row[5])
            texts.append(row[15])
        csvfile.close()
    return (sentiments, texts)

sentiments =[]
texts = []

sentiments, texts = read_csv_file('../nltktest/data/Sentiment_confident.csv')

data = []
for i in range(len(texts)):
    data.append((texts[i], sentiments[i] ))


X, y = create_tfidf_training_data(data[1000:])

# Split the data into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# Run classifier, using a model that is too regularized (C too low) to see
# the impact on the results
classifier = svm.LinearSVC()
y_pred = classifier.fit(X_train, y_train).predict(X_test)

target_names = ['Positive', 'Neutural', 'Negtive']

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


# Compute confusion matrix
cm = confusion_matrix(y_test, y_pred)
np.set_printoptions(precision=2)
print('Confusion matrix, without normalization')
print(cm)
plt.figure()
plot_confusion_matrix(cm)

# Normalize the confusion matrix by row (i.e by the number of samples
# in each class)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
print('Normalized confusion matrix')
print(cm_normalized)
plt.figure()
plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')

plt.show()