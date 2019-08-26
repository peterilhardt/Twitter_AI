# Functions for interacting with the Google Cloud Natural Language API in Python


def get_sentiment_scores(tweets, client):
    
	from google.api_core.exceptions import InvalidArgument
	from google.cloud.language import enums, types
	import numpy as np
	import time

	score_list = []

	for tweet in tweets:
	    document = types.Document(content = tweet, 
	    						  type = enums.Document.Type.PLAIN_TEXT)
	    
	    try:
	        sentiment = client.analyze_sentiment(document = document)
	    except InvalidArgument:  # Google API-specific error
	        score_list.append(np.nan)
	        continue
	    
	    score = sentiment.document_sentiment.score
	    score_list.append(score)
	    time.sleep(0.1)  # allowed 600 requests per minute from API
	    
	return score_list


