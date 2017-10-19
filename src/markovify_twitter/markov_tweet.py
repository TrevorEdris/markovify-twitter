import argparse
import random
import sys

from markovify_twitter.twitter_util import (
    BEGIN,
    END,
    get_all_tweets,
    post_tweet
)

from markovify_twitter.util import (
    blue,
    green,
    red
)


class MarkovTweet():

    name = 'markov_tweet'
    description = '''
    Generate a random tweet based off the tweet history of other users
    '''

    MAX_KEY_LENGTH = 10
    MAX_OVERLAP_RATIO = 0.5
    MAX_OVERLAP_TOTAL = 15
    MAX_CHARS = 140

    rejoined_text = ''
    rejoined_text_lower = ''

    def __init__(self):
        self.parser = self.create_parser()

    def build_markov_chain_from_tweets(self, tweets, key_length, chain=None):
        """
        Builds a markov chain in the form of a dict based off the
        input tweets

        :param tweets: List of lists; Outer list is list of tweets,
                       inner list is list of words in a tweet
        :param key_length: Number of words to use in the chain
        :param chain: Existing chain or None.
                      Multiple chains can be combined.
            EXAMPLE:
                build_markov_chain_from_tweets(trump_tweets, 1, build_markov_chain_from_tweets(bernie_sanders_tweets, 1))
        """
        if chain is None:
            chain = {}

        # Limit the key length since at some point, original tweet
        # generation will be impossible
        if key_length > self.MAX_KEY_LENGTH:
            key_length = self.MAX_KEY_LENGTH

        for tweet in tweets:

            index = key_length
            _begin = True
            for i in range(len(tweet) - key_length):

                # Build list of sentence[index]'s previous key_length words
                # to use as a key for the dictionary
                keys = [tweet[index-i] for i in range(key_length, 0, -1)]
                key = ' '.join(keys)

                # Keep track of what words begin a tweet
                if _begin:
                    if BEGIN in chain:
                        chain[BEGIN].append(key)
                    else:
                        chain[BEGIN] = [key]
                    _begin = False

                if key in chain:
                    chain[key].append(tweet[index])
                else:
                    chain[key] = [tweet[index]]
                index += 1

        return chain

    def build_random_tweet(self, chain, key_length, users=[], msg_len=25, tries=10):
        """
        Attemps to generate a random tweet based off the chain

        :param chain: The markov chain to use
        :param key_length: The number of words in the chain's keys
            * NOTE: Needs to be the same as what was used for build_markov_chain_from_tweets
        :param msg_len: Maximum number of words in the tweet
        :param tries: Maximum number of attempts to generate an original tweet
        """
        for i in range(tries):

            # Get a key from the words that begin a sentence
            words = random.choice(chain[BEGIN]).split(' ')
            sentence = words[0].capitalize()
            if key_length > 1:
                sentence += ' ' + ' '.join(words[1:])

            # Generate a maximum of msg_len words for the sentence
            invalid = False
            for i in range(msg_len - key_length - len(users)):
                try:
                    next_word = random.choice(chain[' '.join(words)])
                    if next_word == END:
                        sentence += f' {" ".join("@" + u for u in users)}'
                        if self.test_generated_tweet(sentence.split(' ')):
                            return sentence, True
                        else:
                            invalid = True
                            break
                    sentence += ' ' + next_word
                    del words[0]
                    words.append(next_word)
                except KeyError:
                    # Print something to let user know an error occured
                    print('t(\'-\')t', end='')

            # If here, reached msg_len OR invalid sentence
            # Make sure sentence ends with punctuation
            if not invalid:
                if not sentence[-1] in '.?!':
                    sentence += random.choice(list('.?!'))
                sentence += f' {" ".join("@" + u for u in users)}'
                if self.test_generated_tweet(sentence.split(' ')):
                    return sentence, True

        return 'UNABLE TO GENERATE ORIGINAL TWEET', False

    def test_generated_tweet(self, words, max_chars=140):
        """
        Checks if the generated tweet was original or not

        :param words: List of words in the tweet
        :param max_chars: Maximum number of characters in the tweet
        """

        # If too many words overlap with a sentence
        # direct from the text, reject that sentence.
        combined = ' '.join(words)
        if len(combined) > 140:
            return False
        overlap_ratio = int(round(self.MAX_OVERLAP_RATIO * len(words)))
        overlap_max = min(self.MAX_OVERLAP_TOTAL, overlap_ratio)
        overlap_over = overlap_max + 1
        gram_count = max((len(words) - overlap_max), 1)
        grams = [words[i:i+overlap_over] for i in range(gram_count)]
        for g in grams:
            gram_joined = ' '.join(g)
            if gram_joined.lower() in self.rejoined_text_lower:
                return False
        return True

    def run(self, args=None):

        if not args.users:
            sys.stderr.write('Users is a required argument')
            self.parser.print_usage()
            sys.exit(1)

        users = args.users
        key_length = args.key_length or 1

        tweets = []
        for user in users:
            tweets += get_all_tweets(user)

        self.rejoined_text = '\n'.join([' '.join([word for word in tweet]) for tweet in tweets])
        self.rejoined_text_lower = self.rejoined_text.lower()

        title = f' Tweet from {" and ".join(users)} '
        s = f' {title}--> key_len: {args.key_length} '
        title = f'{s:=^80}'

        chain = self.build_markov_chain_from_tweets(tweets, key_length)
        random_tweet, original = self.build_random_tweet(chain, key_length, users=users)
        print(blue('\n' + title + '\n'))
        if original:
            print(green(random_tweet))
            tweet_or_nah = input('Post to twitter? (Y/n): ')
            if tweet_or_nah.lower() in ['y', 'yes', 'yeah', 'yup', 'yeppers']:
                print('Posting to twitter...')
                post_tweet(random_tweet)
                print('Done.')
        else:
            print(red(random_tweet))

    def create_parser(self):
        parser = argparse.ArgumentParser(description='''
        Generates a random tweet based off another user's tweets''')
        parser.add_argument('users', type=str, nargs='+', metavar='U',
                help='Usernames of twitter accounts to build tweets from (space-separated list, unamea unameb unamec)')
        parser.add_argument('-k', '--key_length', type=int,
                help='Number of words to use as key in the chain, max of 10')
        return parser

    @classmethod
    def main(cls):
        me = cls()
        return me.run(me.parser.parse_args())


# if __name__ == '__main__':
#    print('Out of date usage')
#    parser = argparse.ArgumentParser(description='''
#    Generates a random tweet based off another user's tweets''')
#    parser.add_argument('users', type=str, nargs='+', metavar='U',
#            help='Usernames of twitter accounts to build tweets from (space-separated list, unamea unameb unamec)')
#    parser.add_argument('-k', '--key_length', type=int,
#            help='Number of words to use as key in the chain, max of 10')
#    args = parser.parse_args()
#
#    users = args.users
#
#    if not args.key_length:
#        args.key_length = 1
#
#    entry_point(users, args.key_length)
#    exit()
#
#    tweets = []
#    for user in users:
#        tweets += get_all_tweets(user)
#    rejoined_text = '\n'.join([' '.join([word for word in tweet]) for tweet in tweets])
#    rejoined_text_lower = rejoined_text.lower()
#
#    title = f' Tweet from {" and ".join(users)} '
#    s = f' {title}--> key_len: {args.key_length} '
#    title = f'{s:=^80}'
#
#    chain = build_markov_chain_from_tweets(tweets, args.key_length)
#    random_tweet, original = build_random_tweet(chain, args.key_length, users=users)
#    print(blue('\n' + title + '\n'))
#    if original:
#        print(green(random_tweet))
#        tweet_or_nah = input('Post to twitter? (Y/n): ')
#        if tweet_or_nah.lower() in ['y', 'yes', 'yeah', 'yup', 'yeppers']:
#            print('Posting to twitter...')
#            post_tweet(random_tweet)
#            print('Done.')
#    else:
#        print(red(random_tweet))
