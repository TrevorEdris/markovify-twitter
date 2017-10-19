#!/usr/bin/env python
# encoding: utf-8
# SOURCE: https://gist.github.com/yanofsky/5436496

import os
import sys

import tweepy  # https://github.com/tweepy/tweepy


# Twitter API credentials
# Register your twitter account as a developer account
# Create a twitter app
consumer_key = os.environ['TWITTER_API_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_API_CONSUMER_SECRET']
access_key = os.environ['TWITTER_API_ACCESS_KEY']
access_secret = os.environ['TWITTER_API_ACCESS_SECRET']

# Delimiters
BEGIN = '__BEGIN__'
END = '__END__'

# Output path to store tweets
TWEET_STASH_DIR = 'tweet_stash'


def get_all_tweets(screen_name):
    """
    Gets all the tweets for the specified user

    :param screen_name: Username
    :returns: List of tweets, where each tweet is a list of words
    """

    if not os.path.exists(TWEET_STASH_DIR):
        os.mkdir(TWEET_STASH_DIR)

    if os.path.exists(f'{TWEET_STASH_DIR}/{screen_name}_tweets.csv'):
        with open(f'{TWEET_STASH_DIR}/{screen_name}_tweets.csv') as fp:
            lines = fp.readlines()
        return [[word.replace('\n', '') for word in line.split(' ')] for line in lines]

    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    try:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    except Exception:
        sys.stderr.write(f'ERROR: User {screen_name} not found\n')
        sys.exit(1)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f'getting tweets before {oldest}')

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f'...{len(alltweets)} tweets downloaded so far')

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [tweet.text.replace('\n', ' ') for tweet in alltweets]
    outtweets = [f'{tweet} {END}' for tweet in outtweets]
    outtweets = [[word.strip() for word in tweet.split(' ')] for tweet in outtweets]

    # write the csv
    with open(f'{TWEET_STASH_DIR}/{screen_name}_tweets.csv', 'w') as f:
            for tweet in outtweets:
                tweet_str = ' '.join(tweet)
                f.write(f'{tweet_str}\n')

    return outtweets


def post_tweet(tweet):
    """
    Posts the tweet to twitter

    :param tweet: The tweet to publish
    """
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    api.update_status(tweet)


if __name__ == '__main__':
    # pass in the username of the account you want to download
    tweets = get_all_tweets("TrevorEdris")
    # Write them out to a file if wanted
