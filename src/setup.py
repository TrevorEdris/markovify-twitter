import os

from setuptools import setup, find_packages


cwd = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(cwd, 'requirements.txt')) as fp:
    requires = fp.readlines()

setup(
    name='markovify_twitter',
    version='0.1.6',
    description='Generate random tweets using markov chains',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    author='Trevor Edris',
    author_email='trevor.edris@gmail.com',
    url='https://github.com/TrevorEdris/markovify_twitter',
    packages=find_packages(exclude=['contrib', 'docs', 'test*', 'tests', '*.tests', '*.tests.*']),
    zip_safe=False,
    extras_require={
        'testing': ['coverage', 'pytest', 'pytest-cov'],
    },
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'markov_tweet = markovify_twitter.markov_tweet:MarkovTweet.main',
        ],
    }
)
