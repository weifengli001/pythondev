from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
import nltk



pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]

neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]

tweets =[]
for(words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

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


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


#print(word_features)

training_set = nltk.classify.apply_features(extract_features,tweets )

classifier = nltk.NaiveBayesClassifier.train(training_set)

tweet = 'Jack is my friend'
tweet = 'girl'
#print(classifier.classify(extract_features(tweet.split())))

test_tweets = [
    (['feel', 'happy', 'this', 'morning'], 'positive'),
    (['larry', 'friend'], 'positive'),
    (['not', 'like', 'that', 'man'], 'negative'),
    (['house', 'not', 'great'], 'negative'),
    (['your', 'song', 'annoying'], 'negative')]

testing_set = nltk.classify.apply_features(extract_features, test_tweets)

for (tweet, sentiment) in test_tweets:
    print(classifier.classify(extract_features(tweet)))

print(nltk.classify.accuracy(classifier, testing_set))

classifier.show_most_informative_features(5)



"""
pipeline = Pipeline([('tfidf', TfidfTransformer()),
                      ('chi2', SelectKBest(chi2, k='all')),
                      ('nb', MultinomialNB())])
"""
pipeline = Pipeline([('tfidf', TfidfTransformer()),
                      ('chi2', SelectKBest(chi2, k='all')),
                      ('nb', MultinomialNB())])

classif = SklearnClassifier(pipeline)

classif.train(training_set)

print(classif.labels())
for (tweet, sentiment) in test_tweets:
    print(classif.classify(extract_features(tweet)))

print(nltk.classify.accuracy(classif, testing_set))
