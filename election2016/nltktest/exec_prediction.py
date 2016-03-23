from sklearn.externals import joblib
import nltk

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
import csv, random, nltk, os, re
from sklearn.externals import joblib




tweets = joblib.load('tweets.pkl')


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




def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

classif = joblib.load('classif.pkl')


def filt_text(text):
    #Remove hyperlinks
    temp = re.sub(r'https?:\/\/.*\/[a-zA-Z0-9]*', '', text)
    #Remove quotes
    #temp = re.sub(r'&amp;quot;|&amp;amp', '', temp)
    #Remove citations
    temp = re.sub(r'@[a-zA-Z0-9]*', '', temp)
    #Remove tickers
    temp = re.sub(r'\$[a-zA-Z0-9]*', '', temp)
    #Remove numbers
    temp = re.sub(r'[0-9]*','',temp)
    temp = temp.encode('ascii', 'ignore')
    words_filtered = [e.lower() for e in temp.split() if len(e) >= 3]
    return words_filtered

#for filename in os.listdir(os.getcwd()):
for filename in ['myprefix.20160316-213339.csv']:
        if not filename.endswith('.csv'):
            continue
        out_filename = filename[:-4]
        out_file = csv.writer(open(out_filename + "_result.csv", "w+"))
        with open(filename) as f:
            myreader = csv.reader(f, delimiter=',')
            for row in myreader:
                row.append(classif.classify(extract_features(filt_text(row[1]))))
                out_file.writerow(row)





"""
for (tweet, sentiment) in tweets:
    print(classif.classify(extract_features(tweet)))
"""