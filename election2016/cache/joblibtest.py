from sklearn.externals import joblib
import pickle
from sklearn.externals import joblib
import nltk

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
import csv, random, nltk
from sklearn.externals import joblib


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


sentiments, texts = read_csv_file('../nltktest/data/Sentiment.csv')

data = []
for i in range(len(texts)):
    data.append((texts[i], sentiments[i] ))

tweets =[]

for(words, sentiment) in data:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

random.shuffle(tweets)

#using joblib caching data
#joblib.dump(tweets, 'tweets.pkl')


t = joblib.load('tweets.pkl')
print(len(t))
