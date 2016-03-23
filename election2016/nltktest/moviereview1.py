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


ids, sentiments = read_csv_file('./data/sentiment_labels.txt', '|')


ids1, texts = read_csv_file('./data/sentlex_exp12.txt')

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

print(tweets[:1])