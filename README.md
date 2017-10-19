# markovify_twitter
Generates random tweets based of a specific user's twitter history

## Requirements

* Python 3.6
* tweepy
  ```shell
  pip install tweepy
  ```

## Installation

Run the provided install script

```shell
./install
```

This script assumes that you have a virtual environment active. If you are not sure what a virtual
environment is, check out this link https://virtualenvwrapper.readthedocs.io/en/latest/

If you do not wish to use a virtual environment, then run this command. In general though,
a virtual environment is recommended to avoid package version conflicts with other projects.

```shell
./install no-venv
```


## USAGE

```shell
markov_tweet <twitter_username>
markov_tweet <twitter_username0> <twitter_username1>
markov_tweet <twitter_username> -k <1 | 2 | 3>
markov_tweet -h
```

### Examples

```shell
markov_tweet realDonaldTrump -k 2
```
```
==================  Tweet from realDonaldTrump --> key_len: 2 ==================

I never said for years (I said no), is now on Island. Food and water on site. @realDonaldTrump
Post to twitter? (Y/n): y
Posting to twitter...
Done.
```

Multiple usernames can be combined to generate a tweet from the combined markov chain from both users

```shell
markov_tweet realDonaldTrump officialjaden -k 1
```

```

=========  Tweet from realDonaldTrump and officialjaden --> key_len: 1 =========

Have the Global Retail Launch Any Magazine Ever Ready? @realDonaldTrump @officialjaden
Post to twitter? (Y/n): y
Posting to twitter...
Done.
```


### Example on twitter

Here is a link to the twitter account that I linked the program to from my laptop. Your version
will not be able to tweet directly from this account, since tweeting directly from code requires
a dev twitter account (free to set up) as well as an API key (also free to set up).
https://twitter.com/MarkovifyErthng

If you are interested in setting one up for yourself, check out these links:
https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens
https://apps.twitter.com/


## TODO

* Prune out the Rt tag
* Add option to store generated tweets
* Add option to tweet a previously generated tweet
* Add tests
* Fix the installed package name
