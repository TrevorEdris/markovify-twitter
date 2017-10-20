import pytest

from markovify_twitter.util import (
    get_word_frequency,
    remove_words,
    sanitize,
    TWITTER_MENTION_PATTERN,
    URL_PATTERN
)


@pytest.mark.parametrize('list_of_words, words_to_remove, patterns_to_remove, expected_result', [
    ([], [], [], []),
    (['A'], ['a'], [], []),
    (['☃'], [], [], ['☃']),  # ☃ http://unicodesnowmanforyou.com/ ☃
    (['longer', 'list', 'of', 'shitey', 'words'], ['shitey'], [], ['longer', 'list', 'of', 'words']),
    (['https://some_url.com'], [], [URL_PATTERN], []),
    (['@Some_shitey-username.001'], [], [TWITTER_MENTION_PATTERN], []),
    (['leave@me'], [], [TWITTER_MENTION_PATTERN], ['leave@me']),
    (['hey,', '@some_user,', 'get', 'a', 'life'], [], [TWITTER_MENTION_PATTERN], ['hey,', 'get', 'a', 'life']),
    (['@some.user', 'look', 'at', 'this', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'], [], [TWITTER_MENTION_PATTERN, URL_PATTERN], ['look', 'at', 'this']),
])
def test_remove_words(list_of_words, words_to_remove, patterns_to_remove, expected_result):
    result = remove_words(list_of_words, words_to_remove, patterns_to_remove)
    assert result == expected_result


@pytest.mark.parametrize('text, expected_result', [
    ('', {}),
    ('Some text here', {'Some': 1, 'text': 1, 'here': 1}),
    ('A a a b', {'A': 1, 'a': 2, 'b': 1}),
])
def test_get_word_frequency(text, expected_result):
    result = get_word_frequency(text)
    assert result == expected_result


@pytest.mark.parametrize('word, expected_result', [
    ('', ''),
    ('\n\t\r()<>\'\"', ''),
    ('Some.! text?, with:; lots@# of$% chars^&*_=+', 'Some.! text?, with:; lots@# of$% chars^&*_=+'),
])
def test_sanitize(word, expected_result):
    result = sanitize(word)
    assert result.strip() == expected_result.strip()
