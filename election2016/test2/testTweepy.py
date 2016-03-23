import tweepy
from test1.myauth import Myauth
from twython import Twython
import json

api = tweepy.API(Myauth.auth)

"""
public_tweets = api.home_timeline(1000)
for tweet in public_tweets:
    print(tweet.text)
"""
consumer_key = 'O6SiTAkcuTLBahfSNaESbdjDb'
consumer_secret = 'WsI4HkMKaKNE2BzHLep7BFckYl9d93onFFTkMqtZsxbn63JCSw'
access_token = '2868107255-jyI0ASuGgzovt9wGfUMNm0Nsrlx6sM1nDMALrNT'
access_secret = 'vLjG4JvjE7t27JnhqFEQiZXjawTplVXZImxEY5rfLOGK6'

twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)

status = twitter.show_status(id='126402758403305474')
status = twitter.show_status()
print(status['text'])
#print(json.dumps(status))

