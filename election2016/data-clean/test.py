import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer

import string


tokenization_pattern = r'''(?x)    # set flag to allow verbose regexps
([A-Z]\.)+        # abbreviations, e.g. U.S.A.
| \w+(-\w+)*        # words with optional internal hyphens
| \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
| \w+[\x90-\xff]  # these are escaped emojis
| [][.,;"'?():-_`]  # these are separate tokens
'''
word_tokenizer = nltk.tokenize.regexp.RegexpTokenizer(tokenization_pattern)

s1 = "On a $50,000 mortgage of 30 years at 8 percent, the monthly payment would be $366.88."

print(word_tokenize(s1))

print (word_tokenizer.tokenize(s1))


s2 ="b'RT @neilpX: @jsc1835: Jeb Bush says that he earned being called Jeb....???   .#GOPDebates /What an achievement ?!?'"
s3 = "RT @philogaytheist: Is 'political correctness' the new Republican dog-whistle for racism, homophobia and islamophobia all rolled into one?"
b'RT @RWSurferGirl: .@GovChristie Just got his ass served to him by @RandPaul  #GOPDebates  #GOPDebates'
b'Dammit these commercial breaks do not measure up with my bathroom breaks. #GOPDebates'
b'RT @kwrcrow: @FoxNews taking huge cheap shots @realDonaldTrump. #ChrisWallace even asking for help from @marcorubio to pound on #Trump. #GO'
b'Rand Paul comes across as the bad guy in a John Hughes film. #GOPDebates https://t.co/OODBonYfa9'
b'RT @b140_tweet: Rip  #AnnRichards... She has it right.. We needed her for President #GOPDEBATES #STOPRUSH http://t.co/uw5AXjzMXC'

tknzr = TweetTokenizer()

print(tknzr.tokenize(s2))

nopunct = [w for w in s2 if w not in string.punctuation]
print(''.join(nopunct[0:100]))