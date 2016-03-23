from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import csv

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



sentiments, texts = read_csv_file('../../nltktest/data/Sentiment_confident.csv')


tvect = TfidfVectorizer(min_df=1, max_df=1)

X = tvect.fit_transform(texts[1000:])

classifier = LinearSVC()
classifier.fit(X, sentiments[1000:])

X_test=tvect.transform(texts[:1000])
print(classifier.predict(X_test))
