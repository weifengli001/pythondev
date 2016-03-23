from nltk.corpus import twitter_samples
from nltk.twitter import Twitter
from nltk.twitter.common import json2csv
import pandas as pd

"""
input_file = twitter_samples.abspath("tweets.20150430-223406.json")
with open(input_file) as fp:
    json2csv(fp, 'tweets.20150430-223406.tweet.csv',
            ['created_at', 'favorite_count', 'id', 'in_reply_to_status_id',
            'in_reply_to_user_id', 'retweet_count', 'retweeted',
            'text', 'truncated', 'user.id'])

for line in open('tweets.20150430-223406.tweet.csv').readlines()[:5]:
    print(line)

tweets = pd.read_csv('tweets.20150430-223406.tweet.csv', index_col=0, header=0, encoding="utf8")
print(tweets.head(5))
"""

