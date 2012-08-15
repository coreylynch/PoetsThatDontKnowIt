This bot builds haikus on the fly from a sample of the twitter public timeline. It uses Blei's implementation of online LDA to assign tweets one of 200 topics (which vary over time). If it can find two other tweets with the same topic and compatible syllables (i.e. 5-7-5), it concatenates them into a haiku and pushes the haiku to the twitter handle over tweepy, while giving full attribution to the original authors. If it can't find suitable matches, the tweet is stored in mongodb alongside its assigned topic (and hashtag if available), and the process continues.

Dependencies:

Tweetstream
NLTK
Tweepy