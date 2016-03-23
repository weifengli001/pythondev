from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify.maxent import MaxentClassifier
import csv, random, nltk, string, re
from sklearn.externals import joblib
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from time import time
import utils.helper
import pylab as pl


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

tweets =[]

for(words, sentiment) in data:
    #temp = temp.encode('ascii', 'ignore')
    tweets.append((list(set(words.split())), sentiment))

random.shuffle(tweets)

tweets = tweets[:2000]

print('tweets num: ', len(tweets))

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist =nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_tweets(tweets))

word_features = word_features

print('word_features: ', len(word_features))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

featuresets = [(extract_features(d), c) for (d, c) in tweets]
print('featuresets: ', len(featuresets))
train_set, test_set = featuresets[:1900], featuresets[1900:]



#Multinomial Naive Bayes classifier
pipeline = Pipeline([('tfidf', TfidfTransformer()),
                      ('chi2', SelectKBest(chi2, k='all')),
                      ('nb', MultinomialNB())])

classif = SklearnClassifier(pipeline)
classif.train(train_set)


#Max entropy classifier
"""
classif = MaxentClassifier.train(train_set, 'megam')
"""
print(nltk.classify.accuracy(classif, test_set))

pred = classif.classify_many([feature for feature, sentiment in test_set])
test_true = [sentiment for feature, sentiment in test_set]
matx = confusion_matrix(test_true,pred)
print(matx)



#joblib.dump(tweets, 'tweets.pkl')
#joblib.dump(classif, 'classif.pkl')





