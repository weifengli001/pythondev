import tweepy

consumer_key = 'O6SiTAkcuTLBahfSNaESbdjDb'
consumer_secret = 'WsI4HkMKaKNE2BzHLep7BFckYl9d93onFFTkMqtZsxbn63JCSw'
access_token = '2868107255-jyI0ASuGgzovt9wGfUMNm0Nsrlx6sM1nDMALrNT'
access_secret = 'vLjG4JvjE7t27JnhqFEQiZXjawTplVXZImxEY5rfLOGK6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
places = api.geo_search(query="United States", granularity="country")
place_id = places[0].id

tweets = api.search(q="place:%s" % place_id)
#tweets = api.search(q='#nlproc', result_type='recent', lang='en', count=10)
for tweet in tweets:
    #print(tweet.text.encode('unicode_escape') + " \n\n " +  tweet.place.name if tweet.place else "Undefined place")
    print(tweet.text)
    print(tweet.text.encode('unicode_escape'))