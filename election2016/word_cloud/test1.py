#!/usr/bin/env python2
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
from wordcloud import WordCloud
import  re

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, '/Users/weifengli/PycharmProjects/election2016/nltktest/prediction_result.csv')).read()

text = re.sub(r'https?:\/\/.*\/[a-zA-Z0-9]*', '', text)
text = re.sub(r'RT', '', text)
text = re.sub(r'Positive', '', text)
text = re.sub(r'Negative', '', text)
text = re.sub(r'Neutral', '', text)
text = re.sub(r'hillary', '', text)
text = re.sub(r'clinton', '', text)
text = re.sub(r'donald', '', text)
text = re.sub(r'trump', '', text)
text = re.sub(r'bernie', '', text)
text = re.sub(r'sander', '', text)
text = re.sub(r'Mar', '', text)
text = re.sub(r'Tue', '', text)
text = re.sub(r'Time', '', text)

# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
#plt.imshow(wordcloud)
#plt.axis("off")

# take relative word frequencies into account, lower max_font_size
wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# The pil way (if you don't have matplotlib)
#image = wordcloud.to_image()
#image.show()