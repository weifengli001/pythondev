from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from textblob.classifiers import NaiveBayesClassifier
from textblob.classifiers import PositiveNaiveBayesClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
import csv, random, nltk
from sklearn.externals import joblib

from textblob import Blobber



train = [
     ('I love this sandwich.', 'pos'),
    ('this is an amazing place!', 'pos'),
     ('I feel very good about these beers.', 'pos'),
     ('this is my best work.', 'pos'),
     ("what an awesome view", 'pos'),
     ('I do not like this restaurant', 'neg'),
     ('I am tired of this stuff.', 'neg'),
     ("I can't deal with this", 'neg'),
     ('he is my sworn enemy!', 'neg'),
     ('my boss is horrible.', 'neg'),
    ("it's not the best.", 'neg'),
    ('it is not good.', 'neg'),
    ('it is not the worst.', 'pos')
 ]
test = [
     ('the beer was good.', 'pos'),
     ('I do not enjoy my job', 'neg'),
     ("I ain't feeling dandy today.", 'neg'),
     ("I feel amazing!", 'pos'),
     ('Gary is a friend of mine.', 'pos'),
    ("I can't believe I'm doing this.", 'neg')
]




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

tweets = tweets[:100]

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
train_set, test_set = featuresets[:80], featuresets[80:]

blob = TextBlob("It's not the worst.", analyzer=NaiveBayesAnalyzer())
print(blob.sentiment)
blob = TextBlob("It's not the worst")
print(blob.sentiment)


cl = NaiveBayesClassifier(train)
print(cl.classify("It's not the worst"))



#tb = Blobber(analyzer=NaiveBayesAnalyzer())


#print(tb("DonaldTrump under fire for comments about women  weigh in on").sentiment)

