from nltk.corpus import names
import nltk
import random

def gender_features(name):
    #return {'last_letter': name[-1]}
    return {'suffix1': name[-1:],
            'suffix2': name[-2:]}

def gender_features2(name):
    features = {}
    features["first_letter"] = name[0].lower()
    features["laster_letter"] = name[-1].lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
        features["has({})".format(letter)] = (letter in name.lower())
    return features


labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
    [(name, 'female') for name in names.words('female.txt')])
random.shuffle(labeled_names)

featuresets = [(gender_features(name), gender) for (name, gender) in labeled_names]

train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(classifier.classify(gender_features('Neo')))
print(classifier.classify(gender_features('Trinity')))

print(nltk.classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(5)

featuresets1 =[(gender_features2(n), gender) for (n, gender) in labeled_names]
train_set1, test_set1 = featuresets1[500:], featuresets1[:500]
classifier1 = nltk.NaiveBayesClassifier.train(train_set1)
print(nltk.classify.accuracy(classifier1, test_set1))

#print(classifier1.show_most_informative_features(5))

train_names = labeled_names[1500:]
devtest_names = labeled_names[500:1500]
test_names = labeled_names[:500]

train_set = [(gender_features(n), gender) for (n, gender) in train_names]
devtest_set = [(gender_features(n), gender) for (n, gender) in devtest_names]
test_set = [(gender_features(n), gender) for (n, gender) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, devtest_set))

errors = []
for (name, tag) in devtest_names:
    guess = classifier.classify(gender_features(name))
    if(guess != tag):
        errors.append((tag, guess, name))
"""
for (tag, guess, name) in sorted(errors):
    print('correct={:<8} guess={:<8s} name={:<30}'.format(tag, guess, name))
"""
print(nltk.classify.accuracy(classifier, test_set))