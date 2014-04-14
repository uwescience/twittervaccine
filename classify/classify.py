#!/usr/bin/env python

"""Tweet sentiment analysis."""

import collections
import random
import sys
import time

import nltk
import nltk.classify

import ttokenize
from extract import *
from tweet import *

def get_instance(tweet):
    """Return a tuple of (feature_dictionary, label)."""
    toks = ttokenize.tokenize(tweet.text)
    feature_dict = dict([(t, True) for t in toks])
    return (feature_dict, tweet.get_majority_vote())

def get_instances(tweets):
    """Return a list of (feature_dictionary, label) tuples."""
    return [get_instance(tweet) for tweet in tweets]

def train_nltk(module, tweets):
    instances = get_instances(tweets)
    return module.train(instances)

def test_nltk(classifier, tweets):
    references = []
    predictions = []
    for tweet in tweets:
        features, label = get_instance(tweet)
        references.append(label)

        predictions.append(classifier.classify(features))

    return nltk.ConfusionMatrix(references, predictions)

TEST_SET_PROPORTION = .2

def main():
    random.seed(7)

    # AAA: Use a random shuffle to select test/training sets
    print('Extracting twitter data from the database...')
    tm1 = time.time()
    tweets = extract()
    tm2 = time.time()

    print('  time=%0.3fs' % (tm2 - tm1))

    test_set_size = int(TEST_SET_PROPORTION * len(tweets))

    print('Training on %d tweets' % (len(tweets) - test_set_size))

    tm1 = time.time()
    random.shuffle(tweets)

    test_set = tweets[:test_set_size]
    training_set = tweets[test_set_size:]

    classifier = train_nltk(nltk.classify.NaiveBayesClassifier, training_set)
    tm2 = time.time()

    print('  time=%0.3fs' % (tm2 - tm1))

    print('Testing accuracy on %d tweets' % test_set_size)
    tm1 = time.time()
    mat = test_nltk(classifier, test_set)
    tm2 = time.time()

    print mat.pp(show_percents=True)
    print ('%d of %d correct ==> %f%%' % (mat._correct, mat._total,
                                          float(mat._correct) / mat._total))
    print('  time=%0.3fs' % (tm2 - tm1))

if __name__ == '__main__':
    main()
