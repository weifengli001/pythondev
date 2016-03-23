import re, csv,os


training_file = '../nltktest/data/Sentiment_confident.csv'
raw_data_file_path = '../datacollection/streaming_data'

set1 = ['hillary', 'clinton',  'hillary clinton']
set2 = ['bernie', 'sanders',  'bernie sanders']
set3 = ['donald', 'trump',  'donald trump']

target_names = ['Positive', 'Neutural', 'Negtive']

def text_filter(text):
    #Remove hyperlinks
    temp = re.sub(r'https?:\/\/.*\/[a-zA-Z0-9]*', '', text)
    #Remove quotes
    #temp = re.sub(r'&amp;quot;|&amp;amp', '', temp)
    #Remove citations
    temp = re.sub(r'@[a-zA-Z0-9]*', '', temp)
    #Remove tickers
    temp = re.sub(r'\$[a-zA-Z0-9]*', '', temp)
    #Remove numbers
    temp = re.sub(r'[0-9]*','',temp)

    #temp = str(temp).encode('ascii', 'ignore')

    l = [e.lower() for e in temp.split() if len(e) >= 3 and
                      'http' not in e
                                and not e.startswith('@')
                                and not e.startswith('#')
                                and e != 'RT']
    return ' '.join(l)

def make_tag(text):
    f, tag = False, ''
    words = set(re.split('\W', text))
    f1 = False
    f2 = False
    f3 = False
    for word in set1:
        if word in words:
            f1 = True
    for word in set2:
        if word in words:
            f2 = True
    for word in set3:
        if word in words:
            f3 = True
    if not ((f1 == True and f2 == True) or (f1 == True and f3 == True) or (f2 == True and f3 == True)):
           if f1 == True:
               f, tag = True, 'hillary clinton'
           elif f2 == True:
               f, tag = True, 'bernie sanders'
           elif f3 == True:
               f, tag = True, 'donald trump'
    return f, tag

def convert2num(sentiments):
    temp =[]
    for sentiment in sentiments:
        if sentiment == 'Positive':
            temp.append(0)
        elif sentiment == 'Neutural':
            temp.append(1)
        else:
            temp.append(2)
    return temp


def read_csv_file(filename, sentiment_index, text_index, delimiter = ','):
    sentiments = []
    texts =[]
    with open(filename) as csvfile:
        myreader = csv.reader(csvfile,delimiter=delimiter)
        for row in myreader:
            sentiments.append(row[sentiment_index])
            texts.append(row[text_index])
        csvfile.close()
    return (sentiments, texts)

def make_data(texts, sentiments):
    data = []
    for i in range(len(texts)):
        data.append((texts[i], sentiments[i] ))
    return data


text_filter('dfwfe  lfe;w*()&()w')