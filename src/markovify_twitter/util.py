NORMAL = '\033[00m'
RED = '\033[31m'
GREEN = '\033[92m'
BLUE = '\033[96m'


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
    to_keep = '.!?,i:;@#$%^&*_+= '

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
    book_words = text.split(' ')
    for word in book_words:
        word = sanitize(word)
        if not word:
            continue
        if word in freqs:
            freqs[word] += 1
        else:
            freqs[word] = 1
    return freqs
