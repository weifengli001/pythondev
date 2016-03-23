import json

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

    print(data)
    for i in range(len(data)):
        d = data[i]
        print(d['text'])


parse_tweet_json('../test1/python.json')