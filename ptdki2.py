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
username = ''
password = ''
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


nytrendsjson = json.loads(requests.get('https://api.twitter.com/1/trends/2459115.json').content)[0]['trends']

nytrends = [nytrendsjson[i]['name'] for i in range(len(nytrendsjson))]

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

stopwords=['rt','d','a','q','o','y','el','c','es','se','si','mi','te','ti','n','e','de','la','ai','las','al','para','x','em','m','t','b','hay','p','ku','nu','ni','ya','ga','que','lo','tu','por','pero','via','o','z','l']

for tweet in stream:
    if 'text' in tweet.keys() and len(tweet['text'])>0:
        
        # Capture hashes
        hashes = [i for i in tweet['text'].split() if '#' in i]
        
        # Strip out hashes, RTs, and @'s and see if the sentence is still the same. Take the intersection of tweets
        # that are stripped of symbols and tweets that are stripped of symbols and english sentences
        temptweet = [i.lower() for i in tweet['text'].split() if '#' not in i and 'rt' not in i.lower() and '@' not in i]
        newtweet = [i.lower() for i in tweet['text'].split() if '@' not in i and '#' not in i and nsyl(i)>0 and isword(i)>0 and i not in stopwords]
        if len(newtweet)==len(temptweet):
            if sylcheck(newtweet)==5 and len(first)==0:
                fillline(newtweet,first)
            elif sylcheck(newtweet)==5 and len(first)>0 and len(third)==0:
                fillline(newtweet,third)
            elif sylcheck(newtweet)==7 and len(second)==0:
                fillline(newtweet,second)
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
                time.sleep(60)



