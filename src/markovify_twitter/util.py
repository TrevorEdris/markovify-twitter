import re

NORMAL = '\033[00m'
RED = '\033[31m'
GREEN = '\033[92m'
BLUE = '\033[96m'

TWITTER_MENTION_PATTERN = '[-\"\']*@[a-zA-Z_\.\-0-9:,\'\"]+'
URL_PATTERN = '^(https?:\/\/)?([\da-z\.-_]+)\.([a-z\.]{2,6})([\/\w \.-_]*)*\/?$'


def red(text):
    return f'{RED}{text}{NORMAL}'


def green(text):
    return f'{GREEN}{text}{NORMAL}'


def blue(text):
    return f'{BLUE}{text}{NORMAL}'


def sanitize(word):
    """
    Removes whitespace and parenthetical characters while
    keeping all chars in to_keep

    :param word: The text to sanitize
    :returns: Sanitized text
    """
    to_replace = '\n\t\r()<>\'\"'
    to_keep = '.!?,:;@#$%^&*_+= '

    # Build list of characters to replace
    for char in word:
        if not char.isalnum() and char not in to_keep and char in to_replace:
            to_replace += char
    for char in to_replace:
        word = word.replace(char, ' ')
    return word or ''


def get_word_frequency(text):
    """
    Builds a word: frequency dict based off the text

    :param text: The text to build the frequency dict for
    :returns: Generated frequency dict
    """
    freqs = {}
    book_words = text.split()
    for word in book_words:
        word = sanitize(word)
        if not word:
            continue
        if word in freqs:
            freqs[word] += 1
        else:
            freqs[word] = 1
    return freqs


def remove_words(list_of_words, words_to_remove=[], patterns_to_remove=[]):
    """
    Removes the words in the list words_to_remove from the
    list list_of_words and removes any word that matches a pattern
    in the list patterns_to_remove

    :param list_of_words: List of words to remove from
    :param words_to_remove: List of words that should be removed
        * NOTE: All words should be lower-case
    :param patterns_to_remove: List of regex patterns to remove
    """

    pruned_list = []
    patterns_joined = '|'.join(f'({pattern})' for pattern in patterns_to_remove)
    if patterns_joined:
        p = re.compile(patterns_joined)

    for word in list_of_words:
        append = True

        if word.lower() in words_to_remove:
            append = False

        # This check will short-circuit if patterns_joined is '', which
        # will be the case if patterns_to_remove is an empty list
        if patterns_joined and p.match(word):
            append = False

        if append:
            pruned_list.append(word)
    return pruned_list
