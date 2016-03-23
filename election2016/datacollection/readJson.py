import json
import csv


def parse_tweet_json( filename ):

    # read tweet
    print('opening: ' + filename)
    fp = open( filename, 'rb' )
    # parse json
    try:
        data = []
        with open(filename) as f:
            for line in f:
                data.append(json.loads(line))
    except ValueError:
        raise RuntimeError('error parsing json')


    for i in range(len(data)):
        d = data[i]
        temp = []
        #print(d['id'], d['text'], d['created_at'], d['user']['location'], d['user']['time_zone'])
        temp.append(d['id'])
        temp.append(d['text'])
        temp.append(d['created_at'])
        temp.append(d['user']['location'])
        temp.append(d['user']['time_zone'])
        with open('./streaming_data/myprefix.20160316-213339.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([d['id'],
                             d['text'],
                             d['created_at'],
                             d['user']['location'],
                             d['user']['time_zone']])




parse_tweet_json('./streaming_data/myprefix.20160316-213339.json')