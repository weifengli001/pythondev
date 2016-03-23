from slistener import SListener
import time, tweepy, sys

## authentication
#username = 'liweifeng.liwf@gmail.com' ## put a valid Twitter username here
#password = '99zhadmin' ## put a valid Twitter password here
#auth     = tweepy.auth.AppAuthHandler(username, password)
#api      = tweepy.API(auth)

consumer_key = 'O6SiTAkcuTLBahfSNaESbdjDb'
consumer_secret = 'WsI4HkMKaKNE2BzHLep7BFckYl9d93onFFTkMqtZsxbn63JCSw'
access_token = '2868107255-jyI0ASuGgzovt9wGfUMNm0Nsrlx6sM1nDMALrNT'
access_secret = 'vLjG4JvjE7t27JnhqFEQiZXjawTplVXZImxEY5rfLOGK6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

def main():
    track = ['hillary clinton', 'bernie sanders', 'donald trump']

    listen = SListener(api, 'myprefix')
    stream = tweepy.Stream(auth, listen)

    print("Streaming started...")

    try:
        stream.filter(track = track)
    except:
        print ("error!")
        stream.disconnect()

if __name__ == '__main__':
    main()