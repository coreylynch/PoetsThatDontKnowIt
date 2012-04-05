import nltk
from nltk.corpus import cmudict, wordnet
import tweetstream
import string
import re
import numpy 
import pickle

d = cmudict.dict()
username = ''
password = ''

pkl_file = open('actualdictwithvals.pkl','r')
dictionary = pickle.load(pkl_file)
pkl_file.close()

def nsyl(word):
  try:
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
  except(AttributeError,KeyError, TypeError):
    return 0

def sylcheck(line):
  return sum([nsyl(i) for i in line])

stream = tweetstream.SampleStream(username,password)
urlre = re.compile('(?P<url>https?://[^\s]+)')
punctre = re.compile('[%s]' % re.escape(string.punctuation))


stopwords=['rt','d','a','q','o','y','el','c','es','se','si','mi','te','ti','n','e','de','la','ai','las','al','para','x','em','m','t','b','hay','p','ku','nu','ni','ya','ga','que','lo','tu','por','pero','via','o','z','l']

for i in nltk.corpus.stopwords.words('english'):
  stopwords.append(i)



def main():
  counter=0
  for tweet in stream:
    if 'text' in tweet.keys() and len(tweet['text'])>0:
      tweetstripped = urlre.sub('',tweet['text'])
      tweetstripped = punctre.sub('',tweetstripped)
      temptweet = [i.lower() for i in tweetstripped.split() if '#' not in i and not i.lower().startswith('rt') and '@' not in i]
      newtweet = [i.lower() for i in tweetstripped.split() if '#' not in i and not i.lower().startswith('rt') and '@' not in i and nsyl(i)>0 and i.lower() not in stopwords]
      if len(temptweet)==len(newtweet):
        for i in newtweet:
          if i not in stopwords:
            dictionary[i] = dictionary.setdefault(i,0)+1
            print 'updating: ' + i
            counter +=1
            if (counter % 100 == 0):
              print 'Iteration '+i
              f = open('actualdictwithvals.pkl','w')
              pickle.dump(dictionary,f)


if __name__ == '__main__':
    main()

