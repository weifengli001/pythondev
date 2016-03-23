import csv, random, nltk

sentiments =[]
texts = []
def read_csv_file(filename, delimiter = ','):
    ids = []
    values =[]
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=delimiter)
        for row in reader:
            sentiments.append(row[5])
            texts.append(row[15])
        csvfile.close()
    return (sentiments, texts)


sentiments, texts = read_csv_file('../data/Sentiment.csv')

data = []
for i in range(len(texts)):
    data.append((texts[i], sentiments[i] ))

tweets =[]

for(words, sentiment) in data:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

random.shuffle(tweets)

tweets = tweets[:10000]

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
train_set, test_set = featuresets[:8000], featuresets[8000:]
#print(word_features)
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))







