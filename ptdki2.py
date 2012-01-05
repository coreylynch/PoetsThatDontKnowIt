#Dynamically generates Haikus from Twitter

import nltk
from nltk.corpus import cmudict, wordnet
import tweetstream
import time
import requests
import simplejson as json
import tweepy
import string
import re

def main():
  d = cmudict.dict()
  username = ''
  password = ''
  CONSUMER_KEY = ''
  CONSUMER_SECRET = ''
  ACCESS_TOKEN_KEY = ''
  ACCESS_TOKEN_SECRET = ''

  stream = tweetstream.SampleStream(username,password)

  # Helper Functions
  def posttweet(status):
    if len(status)<=140:
      auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
      auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
      api = tweepy.API(auth)
      result = api.update_status(status)
      return result

  def nsyl(word):
    try:
      return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    except(AttributeError,KeyError, TypeError):
      return 0

  urlre = re.compile('(?P<url>https?://[^\s]+)')
  punctre = re.compile('[%s]' % re.escape(string.punctuation))
  emoticons = [':)',':(','<3',';)',':-)',':-(','=)',':P']

  def sylcheck(line):
    return sum([nsyl(i) for i in line])

  first =[]
  second=[]
  third=[]
  first_user=''
  second_user=''
  third_user=''

  stopwords=['rt','d','a','q','o','y','el','c','es','se','si','mi','te','ti','n','e','de','la','ai','las','al','para','x','em','m','t','b','hay','p','ku','nu','ni','ya','ga','que','lo','tu','por','pero','via','o','z','l']


  for tweet in stream:
    if 'text' in tweet.keys() and len(tweet['text'])>0:
    
      # Capture screen name
      screen_name = '@'+tweet['user']['screen_name']
 
      # Capture hashes and emoticons
      hashes = set([i for i in tweet['text'].split() if i.startswith('#')])
      emoticons = set([i for i in tweet['text'].split() if i in emoticons])
    
      # Strip out urls, punctuation, RTs, and @'s
      tweetstripped = urlre.sub('',tweet['text'])
      tweetstripped = punctre.sub('',tweetstripped)
    
      temptweet = [i.lower() for i in tweetstripped.split() if '#' not in i and not i.lower().startswith('rt') and '@' not in i]
      newtweet = [i.lower() for i in tweetstripped.split() if '#' not in i and not i.lower().startswith('rt') and '@' not in i and nsyl(i)>0 and i.lower() not in stopwords]
    
      if len(newtweet)==len(temptweet):
        if sylcheck(newtweet)==5 and len(first)==0:
          first = list(newtweet)
          first_user = screen_name
        elif sylcheck(newtweet)==5 and len(first)>0 and len(third)==0:
          third = list(newtweet)
          third_user = screen_name
        elif sylcheck(newtweet)==7 and len(second)==0:
          second = list(newtweet)
          second_user = screen_name
        elif sylcheck(first)==5 and sylcheck(second)==7 and sylcheck(third)==5:
          line1 = ' '.join(i.lower() for i in first)
          line2 = ' '.join(i.lower() for i in second)
          line3 = ' '.join(i.lower() for i in third)
          u1 = first_user
          u2 = second_user
          u3 = third_user
          print line1
          print line2
          print line3
          print first_user+', '+second_user+', '+third_user
          print '\n'
          del first[0:len(first)]
          del second[0:len(second)]
          del third[0:len(third)]
          first_user=''
          second_user=''
          third_user=''
          posttweet('"'+line1+' // '+line2+' // '+line3+'"'+' -- '+u1+', '+u2+', '+u3)
          time.sleep(90)


if __name__ == '__main__':
    main()


