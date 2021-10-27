
# Sentiment analysis using TextBlob library

from textblob import TextBlob
import re

def clean_tweet(tweet):
    # Clean text for TextBlob
    return ' '.join(re.sub(r'''(@[A-Za-z0-9_]+)|     # Remove mentions that start with @
                                ([^0-9A-Za-z \t])    # Remove non-alphanumeric (except space and tab) characters
                                |(\w+:\/\/\S+)''',   # Remove web links
                                " ", tweet).split())
    
def analyze_polarity(tweet):
    '''
    Analyze polarity. Returns 1 for positive, 0 for neutral and -1 for negative.
    '''
    analysis = TextBlob(clean_tweet(tweet))

    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

def analyze_subjectivity(tweet):
    '''
    Subjectivity analizer. Returns 1 if tweet is subjective or 0 if tweet is objective
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.subjectivity >= 0.5:
        return 1
    else:
        return 0


# Process tweets for words frequency distribution

import string

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

def process_tweet(tweet):
    """Process tweet function.
    Input:
        tweet: a string containing a tweet
    Output:
        tweets_clean: a list of words containing the processed tweet

    """
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)
    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)
    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    # remove hashtags (only the hashtag symbol)
    tweet = re.sub(r'#', '', tweet)
    # remove punctuation
    tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet)
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)

    tweets_clean = []
    for word in tweet_tokens:
        if word not in stopwords_english:  # remove stopwords
            # stem and add word to tweets_clean list
            stem_word = stemmer.stem(word)  # stemming word
            tweets_clean.append(stem_word)

    return tweets_clean


