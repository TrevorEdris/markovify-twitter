# markovify_twitter
Generates random tweets based of a specific user's twitter history

## Requirements

* Python 3.6
* tweepy
  ```shell
  pip install tweepy
  ```

## USAGE

```shell
python tweet_markov.py <twitter_username0>
```

#### Example

```shell
python tweet_markov.py realDonaldTrump
```

Multiple usernames can be combined to generate a tweet from the combined markov chain from both users

```shell
python tweet_markov.py realDonaldTrump officialjaden
```

## TODO

* setup.py
* Directory structure
* Prune out the Rt tag
