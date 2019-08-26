# Functions for cleaning Twitter text


def remove_stopwords(tweet, stopwords):
	"""
	Removes a pre-defined list of stopwords from a Tweet.

	Parameters
	----------
	tweet: string
		Tweet text
	stopwords: list of strings
		stopwords to be removed

	Returns
	-------
	string
		Tweet text with stopwords removed
	"""

	import re

	stopwords_set = set(stopwords)
	split_tweet = [word for word in re.split('\W+', tweet) if word \
											 not in stopwords_set]
	return ' '.join(split_tweet)

def clean_tweet(tweet, stopwords = []):
	"""
	Takes a Tweet (string) and cleans it by:

	1. Removing numbers and words with numbers in them
	2. Removing all punctuation
	3. Making all letters lowercase
	4. Removing all non-English language characters (e.g. letters with 
	   accents, Chinese symbols, etc.)
	5. Removing Twitter-specific items, including hashtags, mentions, 
	   URLs, emojis, smileys, and Twitter-reserved words ('RT', 'FAV')
	6. Removing one- and two-letter words
	7. Removing undesired stopwords (if any)
	8. Stripping whitespace

	Parameters
	----------
	tweet: string
		Tweet text
	stopwords: list of strings, default: []
		stopwords to be removed (if any)

	Returns
	-------
	string
		Tweet text cleaned
	"""

	import re
	import string
	import preprocessor  # module for preprocessing tweets
						 # https://pypi.org/project/tweet-preprocessor/

	# removes numbers and words with numbers
	remove_numbers = lambda s: re.sub(r'\w*\d+\w*', ' ', s)  
	
	# removes !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
	remove_punctuation = lambda s: re.sub(r'[%s]' % \
							re.escape(string.punctuation), ' ', s)  
	
	# makes all letters lowercase
	lowercase = lambda s: s.lower()  
	
	# removes non-english language characters
	ascii_only = lambda s: re.sub(r'[^\x00-\x7F]+', ' ', s)  
	
	# removes hashtags, mentions, URLs, emojis, smileys, reserved words ('RT')
	remove_twitter_special = lambda s: preprocessor.clean(s)  
	
	# removes 1 and 2 letter words
	remove_short_words = lambda s: re.sub(r'\W*\b\w{1,2}\b', '', s)
	
	clean_tw = lowercase(remove_numbers(remove_punctuation\
				(remove_twitter_special(ascii_only(tweet)))))
	clean_tw = remove_short_words(remove_stopwords(clean_tw, stopwords))
	return clean_tw.strip()

