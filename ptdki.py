#Dynamically generates Haikus from Twitter


import nltk
from nltk.corpus import cmudict, wordnet
import tweetstream
import time
import enchant
import requests
import simplejson as json
import tweepy


d = cmudict.dict()
e = enchant.Dict('en_US')
username = 'TWITTER_USERNAME'
password = 'TWITTER_PASSWORD'
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

def posttweet(status):
  if len(status)<=140:
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    result = api.update_status(status)
    return result

# Some version 2.0 stuff
#nytrendsjson = json.loads(requests.get('https://api.twitter.com/1/trends/2459115.json').content)[0]['trends']
#nytrends = [nytrendsjson[i]['name'] for i in range(len(nytrendsjson))]


# Helper functions
stream = tweetstream.SampleStream(username,password)

def nsyl(word):
  try:
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
  except(AttributeError,KeyError, TypeError):
    return 0

def isword(word):
  if word=='rt':
    return False
  else: 
    return e.check(word)

def fillline(tweet,line):
  for i in tweet:
    line.append(i)

def sylcheck(line):
  return sum([nsyl(i) for i in line])

first =[]
second=[]
third=[]

stopwords=['d','a','q','o','y','el','c','es','se','si','mi','te','ti','n','e','de','la','ai','las','al','para','x','em','m','t','b','hay','p','ku','nu','ni','ya','ga','que','lo','tu','por','pero','via','o','z','l']


# Build Haikus and post to twitter

for tweet in stream:
  if 'text' in tweet.keys() and len(tweet['text'])>0:
    tweet = [i.lower() for i in tweet['text'].split() if nsyl(i)>0 and i.lower() not in stopwords and isword(i.lower())>0]
    if sylcheck(tweet)==5 and len(first)==0:
      fillline(tweet,first)
    elif sylcheck(tweet)==5 and len(first)>0 and len(third)==0:
      fillline(tweet,third)
    elif sylcheck(tweet)==7 and len(second)==0:
      fillline(tweet,second)
    elif sylcheck(first)==5 and sylcheck(second)==7 and sylcheck(third)==5:
      line1 = ' '.join(i.lower() for i in first)
      line2 = ' '.join(i.lower() for i in second)
      line3 = ' '.join(i.lower() for i in third)
      print line1
      print line2
      print line3
      print '\n'
      first=[]
      second=[]
      third=[]
      posttweet(line1+' // '+line2+' // '+line3)
      time.sleep(90)

