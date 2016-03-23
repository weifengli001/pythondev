from sklearn.feature_extraction.text import TfidfVectorizer

docs=[
    ('I love China.', 'positive'),
    ('It tastes bad.', 'negtive'),
    ('I come from China.', 'neutral')
]

y = [d[1] for d in docs]
print(y)

corpus = [d[0] for d in docs]
print(corpus)

vectorizer = TfidfVectorizer(min_df=1)
X = vectorizer.fit_transform(corpus)

print(X)