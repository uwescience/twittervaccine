#!/usr/bin/env python

"""Publish sentiment data to the database."""

import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

import git_rev
from db import get_database_connection

# mapping from algorithm name to code; this really should be stored in the database
ALGORITHMS = { 'vsps': 1, 'afinn111' : 2, 'afinn111_revised' : 3,
	'naivebayes': 4, 'logistic': 5, 'test': 999}

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS sentiment_score(
  id INT, algorithm SMALLINT, revision VARCHAR(64), result FLOAT,
  PRIMARY KEY (id, algorithm, revision));
"""

INSERT_SQL = """
REPLACE INTO sentiment_score_2014(tweet_id, algorithm, revision, result)
VALUES (%s, %s, %s, %s);
"""

def publish_sentiment(algorithm, tweets):
	"""Store a list of sentiment analysis results into the data base.

	:param algorithm: The algorithm used to classify tweets; can be a string or
	or an integer.
	:param tweets: An iterable list of (tweet_id, sentiment_score) tuples.
	"""

	rev = 'xxxxxxx'
	# rev = git_rev.git_current_revision()
	if isinstance(algorithm, str):
		algo = ALGORITHMS[algorithm]
	else:
		algo = algorithm

	conn = get_database_connection(port = 2001)
	cursor = conn.cursor()
	cursor.execute(CREATE_SQL)

	for tweet_id, score in tweets:
		cursor.execute(INSERT_SQL, [tweet_id, algo, rev, score])

	conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
	# create some dummy test data
	tweets = [(1, -.9), (2, -.3), (3, .7), (4, 0.0), (5, 1.1)]
	publish_sentiment('test', tweets)
