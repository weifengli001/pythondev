import tweepy
from tweepy import OAuthHandler


class Myauth:

    consumer_key = 'O6SiTAkcuTLBahfSNaESbdjDb'
    consumer_secret = 'WsI4HkMKaKNE2BzHLep7BFckYl9d93onFFTkMqtZsxbn63JCSw'
    access_token = '2868107255-jyI0ASuGgzovt9wGfUMNm0Nsrlx6sM1nDMALrNT'
    access_secret = 'vLjG4JvjE7t27JnhqFEQiZXjawTplVXZImxEY5rfLOGK6'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    def get_auth(self):
        return self.auth

    def get_api(self):
        api = tweepy.API(self.auth)
        return api