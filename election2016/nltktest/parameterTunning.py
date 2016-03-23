from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify.maxent import MaxentClassifier
import csv, random, nltk, string, re
from sklearn.externals import joblib
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn import svm
import numpy as np
from sklearn import svm, grid_search
from sklearn import linear_model
from sklearn import cross_validation
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report


vectorizer = TfidfVectorizer(min_df=1)
def create_tfidf_training_data(docs):
    """
    Creates a document corpus list (by stripping out the
    class labels), then applies the TF-IDF transform to this
    list.

    The function returns both the class label vector (y) and
    the corpus token/feature matrix (X).
    """
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

sentiments =[]
texts = []
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



sentiments, texts = read_csv_file('./data/Sentiment_confident.csv')

data = []
for i in range(len(texts)):
    data.append((texts[i], sentiments[i] ))


X, y = create_tfidf_training_data(data)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


"""
gammas = np.logspace(-6, -1, 10)
svc = svm.SVC()
clf = grid_search.GridSearchCV(estimator=svc,param_grid=dict(gamma=gammas), n_jobs=-1, refit=True)

clf.fit(X_train, y_train)

print(clf.best_score_)
print(clf.best_params_)
print(clf.best_estimator_.gamma)
"""



###################################################################
#parameter tunning for MultinomialNB
# Set the parameters by cross-validation
tuned_parameters = [{'alpha': []}]

alpha = np.logspace(-6, -1, 10)
nb = MultinomialNB()
clf = grid_search.GridSearchCV(estimator=nb,param_grid=dict(alpha=alpha), n_jobs=-1, refit=True)

clf.fit(X_train, y_train)

predicted = cross_validation.cross_val_predict(clf, X, y, cv=10)
score = metrics.accuracy_score(y, predicted)

#print(score)

#print(clf.best_score_)
#print(clf.best_params_)
#print(clf.best_estimator_)


print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
for params, mean_score, scores in clf.grid_scores_:
    print("%0.3f (+/-%0.03f) for %r"
            % (mean_score, scores.std() * 2, params))
print()

print("Detailed classification report:")
print()
print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")
print()
y_true, y_pred = y_test, clf.predict(X_test)
print(classification_report(y_true, y_pred))
print()





##############################################################################
#tunning SVM model(kernel: linear, rbf)
# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': np.logspace(-6, -1, 10),
                     'C': [1, 10, 100, 1000, 10000, 100000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000, 10000, 100000]}]

scores = ['precision', 'recall']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(SVC(C=1), tuned_parameters, cv=5,
                       scoring='%s_weighted' % score)
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print()
##################################################################