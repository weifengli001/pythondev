from tweepy import Stream
from tweepy.streaming import StreamListener
from test1.myauth import Myauth
import json

class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('python1.json', 'a') as f:
                #all_data = json.load(data)
                #tweet = all_data["text"]
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_daa: %s" % str(e))
        return True

    def on_error(self, status_code):
        print(status_code)
        return True
auth = Myauth().get_auth()
api = Myauth().get_api()
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['Donald Trump'],languages=['en'], locations=[-122.75,36.8,-121.75,37.8,-74,40,-73,41])

