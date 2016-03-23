import csv

with open('./data/Sentiment.csv') as csvfile:
     mreader = csv.reader(csvfile)
     for row in mreader:
         print(row[0])