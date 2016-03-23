import urllib

# pull data
item = ['', '','126366123368267776']
raw_dir = '~/'
url = 'http://api.twitter.com/1/statuses/show.json?id=' + item[2]
urllib.urlretrieve( url, raw_dir + item[2] + '.json' )



https://api.twitter.com/1/statuses/show.json?id=126366123368267776

https://api.twitter.com/1.1/statuses/show.json?id=126366123368267776