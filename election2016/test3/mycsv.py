import csv, re

"""
with open('./data/Sentiment.csv') as csvfile:
     reader = csv.reader(csvfile)
     for row in reader:
         print(row[15].encode('ascii', 'ignore'))
"""

def read_csv_file(filename, delimiter = ','):
    out_filename = 'Test'
    out_file = csv.writer(open(out_filename + "_result.csv", "w+"))
    with open(filename) as csvfile:
        myreader = csv.reader(csvfile,delimiter=delimiter)
        for row in myreader:
            print(row)
            out_file.writerow([row[0],
                              row[1],row[-1]])
    csvfile.close()

read_csv_file('/Users/weifengli/Desktop/prediction_result.csv')

