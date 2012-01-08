#Dynamically generates Haikus from Twitter

import sys
from pymongo import Connection
from pymongo.errors import ConnectionFailure
import nltk
from nltk.corpus import cmudict, wordnet
import tweetstream
import time
import requests
import simplejson as json
import tweepy
import string
import re
import onlineldavb
import numpy
import pycurl

d = cmudict.dict()
USER = 'TWITTER_USER_NAME'
PASS = 'TWITTER_PASS'
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''
STREAM_URL = 'https://stream.twitter.com/1/statuses/sample.json'

stopwords=['rt','d','a','q','o','y','el','c','es','se','si','mi','te','ti','n','e','de','la','ai','las','al','para','x','em','m','t','b','hay','p','ku','nu','ni','ya','ga','que','lo','tu','por','pero','via','o','z','l']
  
urlre = re.compile('(?P<url>https?://[^\s]+)')
punctre = re.compile('[%s]' % re.escape(string.punctuation))

def nsyl(word):
  try:
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
  except(AttributeError,KeyError, TypeError):
    return 0

def sylcheck(line):
  return sum([nsyl(i) for i in line])

def posttweet(status):
  if len(status)<=140:
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    result = api.update_status(status)
    return result

def findmatch(db,tweet,sylcount,hash,topic):
  h = db.tweets.find_one({'sylcount':str(sylcount),'hash':hash})
  if h != None:
    return h
  else:
    t = db.tweets.find_one({'sylcount':str(sylcount),'topic':str(topic)})
    if t != None:
      return t


class Client:  
  def __init__(self):  
   
    # OLDA 
    self.D = 3.3e6
    self.K = 200
    self.vocab = file('./tweetdict.txt').readlines()
    self.W = len(self.vocab)
    self.olda = onlineldavb.OnlineLDA(self.vocab, self.K, self.D, 1./self.K, 1./self.K, 1024., 0.7)
    # Assign lambdas and the counter to the previous iteration
    self.olda._lambda = numpy.loadtxt(sys.argv[1])
    self.counter=int(sys.argv[2])
    
    self.top_words={}  
    for k in range(0,len(self.olda._lambda)):
              lambdak = list(self.olda._lambda[k,:])
              lambdak = lambdak / sum(lambdak)
              temp = zip(lambdak, range(0, len(lambdak)))
              temp = sorted(temp, key = lambda x: x[0], reverse=True)
              self.top_words[str(k)]=self.vocab[temp[0][1]]     

    # Connect to Mongo 
    try:
      c = Connection(host="localhost", port=27017)
      print "Connected successfully"
    except ConnectionFailure, e:
      sys.stderr.write("Could not connect to MongoDB: %s" % e)
      sys.exit(1)
    self.db = c['haiku']
    # Connect to twitter
    self.buffer = ""  
    self.conn = pycurl.Curl()  
    self.conn.setopt(pycurl.USERPWD, "%s:%s" % (USER, PASS))  
    self.conn.setopt(pycurl.URL, STREAM_URL)  
    self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)  
    self.conn.perform()
     
 
  # Open connection to Twitter Real-Time Stream, build Haikus
  def on_receive(self, data):  
    self.buffer += data  
    if data.endswith("\r\n") and self.buffer.strip():  
      tweet = json.loads(self.buffer)  
      self.buffer = ""
      
      if 'text' in tweet.keys() and len(tweet['text'])>0:
        # Capture screen name
        screen_name = '@'+tweet['user']['screen_name']
        # Capture hashes and emoticons
        hashes = [j for j in set([i for i in tweet['text'].split() if i.startswith('#')])]
        # Strip out urls, punctuation, RTs, and @'s
        tweetstripped = urlre.sub('',tweet['text'])
        tweetstripped = punctre.sub('',tweetstripped)
        temptweet = [i.lower() for i in tweetstripped.split() if '#' not in i and not i.lower().startswith('rt') and '@' not in i]
        newtweet = [i.lower() for i in tweetstripped.split() if '#' not in i and not i.lower().startswith('rt') and '@' not in i and nsyl(i)>0 and i.lower() not in stopwords]
        if len(newtweet)==len(temptweet):
          print 'Iteration '+str(self.counter)
         
          #Assign this tweet a topic
          docset = []
          docset.append(' '.join(i for i in newtweet))
          #print 'Tweet: '+docset[0]
          (gamma, bound) = self.olda.update_lambda(docset)
          self.counter+=1
          if (self.counter % 100 == 0):
            numpy.savetxt('lambda-%d.dat' % self.counter, self.olda._lambda)
            numpy.savetxt('gamma-%d.dat' % self.counter, gamma)
            # Save top words
            self.top_words.clear()
            for k in range(0,len(self.olda._lambda)):
              lambdak = list(self.olda._lambda[k,:])
              lambdak = lambdak / sum(lambdak)
              temp = zip(lambdak, range(0, len(lambdak)))
              temp = sorted(temp, key = lambda x: x[0], reverse=True)
              self.top_words[str(k)]=self.vocab[temp[0][1]]
            
          topic = numpy.argmax(gamma)
          

          # For each incoming tweet, look for a hash or topic match in the db that also fits haiku format
          # If none exist, add to the db
          hash = ''
          if sylcheck(newtweet)==5:
            if len(hashes)>0:
              hash=hashes[0]
            t1 = findmatch(self.db,' '.join(i for i in newtweet),7,hash,topic)
            t2 = findmatch(self.db,' '.join(i for i in newtweet),5,hash,topic)
            if t1 != None and t2 != None:
              stanza1 = ' '.join(i for i in newtweet)
              stanza2 = t1['tweet']
              stanza3 = t2['tweet']
              a1 = screen_name
              a2 = t1['author']
              a3 = t2['author']
              if len(hash)>0:
                tweet = hash+': '+'"'+stanza1+' // '+stanza2+' // '+stanza3+'"'+' -- '+a1+', '+a2+', '+a3
              else:
                tweet = '#'+self.top_words[str(topic)]+': '+'"'+stanza1+' // '+stanza2+' // '+stanza3+'"'+' -- '+a1+', '+a2+', '+a3
              
              if stanza1 != stanza3:
                print str(topic)+': '+tweet 
                # Post back to twitter
                posttweet(tweet)

                # clean up
                del hash
                self.db.tweets.remove({'_id':t1['_id']})
                self.db.tweets.remove({'_id':t2['_id']})
            else:
              if len(hash)>0:
                tweet_doc = {'tweet':' '.join(i for i in newtweet),'hash':hash,'topic':str(topic),'sylcount':str(sylcheck(newtweet)),'author':screen_name}
              else:
                tweet_doc = {'tweet':' '.join(i for i in newtweet),'topic':str(topic),'sylcount':str(sylcheck(newtweet)),'author':screen_name}
              # Don't store duplicates
              if self.db.tweets.find_one({'tweet':' '.join(i for i in newtweet)}) == None:
                self.db.tweets.insert(tweet_doc, safe=True)
                print 'Inserting: '+str(topic)+': '+' '.join(i for i in newtweet)
          elif sylcheck(newtweet)==7:
            hash=''
            if len(hashes)>0:
              hash=hashes[0]
            t1 = findmatch(self.db,' '.join(i for i in newtweet),5,hash,topic)
            t2 = findmatch(self.db,' '.join(i for i in newtweet),5,hash,topic)
            if t1 != None and t2 != None:
              stanza2 = ' '.join(i for i in newtweet)
              stanza1 = t1['tweet']
              stanza3 = t2['tweet']
              a2 = screen_name
              a1 = t1['author']
              a3 = t2['author']
              if len(hash)>0:
                tweet = hash+': '+'"'+stanza1+' // '+stanza2+' // '+stanza3+'"'+' -- '+a1+', '+a2+', '+a3
              else:
                tweet = '#'+self.top_words[str(topic)]+': '+'"'+stanza1+' // '+stanza2+' // '+stanza3+'"'+' -- '+a1+', '+a2+', '+a3 
              
              if stanza1!=stanza3: 
                print str(topic)+': '+tweet
                # Post back to twitter    
                posttweet(tweet)
           
              # clean up
              del hash
              self.db.tweets.remove({'_id':t1['_id']})
              self.db.tweets.remove({'_id':t2['_id']})
            else:
              if len(hash)>0:
                tweet_doc = {'tweet':' '.join(i for i in newtweet),'hash':hash,'topic':str(topic),'sylcount':str(sylcheck(newtweet)),'author':screen_name}
              else:
                tweet_doc = {'tweet':' '.join(i for i in newtweet),'topic':str(topic),'sylcount':str(sylcheck(newtweet)),'author':screen_name}
              if self.db.tweets.find_one({'tweet':' '.join(i for i in newtweet)}) == None:
                self.db.tweets.insert(tweet_doc, safe=True)
                print 'Inserting: '+str(topic)+': '+' '.join(i for i in newtweet)

           
if __name__ == '__main__':
    client = Client()

