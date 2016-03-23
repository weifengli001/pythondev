import csv, random, nltk



ids =[]
sentiments =[]

ids1 = []
texts = []
def read_csv_file(filename, delimiter = ','):
    ids = []
    values =[]
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=delimiter)
        for row in reader:
            ids.append(row[0])
            values.append(row[1])
        csvfile.close()
    return (ids, values)


ids, sentiments = read_csv_file('../data/sentiment_labels.txt', '|')


ids1, texts = read_csv_file('../data/sentlex_exp12.txt')

print(len(sentiments))
print(len(texts))

data = []
for i in range(len(texts)):
    data.append((texts[i], 'neg' if float(sentiments[i]) <= 0.4
    else ('pos' if float(sentiments[i]) > 0.6 else 'nut')  ))

tweets =[]

for(words, sentiment) in data:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

random.shuffle(tweets)



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

featuresets = [(extract_features(d), c) for (d, c) in tweets]

train_set, test_set = featuresets[500:], featuresets[:500]
#print(word_features)
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))














