# Functions for interacting with the Google Cloud Natural Language API in Python


def get_sentiment_scores(tweets, client):
	"""
	Calculates sentiment scores for each of a series of Tweets (text inputs) 
	using the Google Cloud Natural Language API. Must have an account setup
	with Google API in order to connect to a client. Returns a list with the
	sentiment scores for each Tweet.

	Parameters
	----------
	tweets: list or Series of strings
		The input text dataset (one string for each document)
	client: google.cloud.language.LanguageServiceClient
		Client connection to the Google Cloud Natural Language API
		Initiate with google.oauth2.service_account.Credentials as needed

	Returns
	-------
	list
		Sentiment scores calculated for each of the input documents
	"""
    
	from google.api_core.exceptions import InvalidArgument
	from google.cloud.language import enums, types
	import numpy as np
	import time

	score_list = []

	for tweet in tweets:  # define document type
	    document = types.Document(content = tweet, 
	    						  type = enums.Document.Type.PLAIN_TEXT)
	    
	    try:
	        sentiment = client.analyze_sentiment(document = document)
	    except InvalidArgument:  # Google API-specific error
	        score_list.append(np.nan)
	        continue
	    
	    score = sentiment.document_sentiment.score # sentiment score
	    score_list.append(score)
	    time.sleep(0.1)  # allowed 600 requests per minute from API
	    
	return score_list


