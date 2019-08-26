# Helpful functions for interacting with the Twitter API using Python


def tweet_to_string(tweet):
    """
    Takes Tweet text in JSON format (dictionary) and converts it to a useful string output.
    
    Parameters
    ---------
    tweet: dictionary
        Tweet in JSON format as returned by requests.get(...).json()
        
    Returns
    -------
    structured string output
        Useful information extracted from the Tweet text
    """
    
    s = """
        Text: {text}
        Hashtags: {hashtags}
        Name: {name} 
        Username: {screenname}
        User Description: {description}
        Social Status: {friends} friends, {followers} followers, {favorites} favorites
        Location: {location}
        Geocode: {geo}
        Date: {date}
    """.format(text = tweet['text'], 
               hashtags = tweet['entities']['hashtags'],
               name = tweet['user']['name'], 
               screenname = tweet['user']['screen_name'],
               description = tweet['user']['description'],
               friends = tweet['user']['friends_count'],
               followers = tweet['user']['followers_count'],
               favorites = tweet['user']['favourites_count'],
               location = tweet['user']['location'],
               geo = tweet['geo'],
               date = tweet['created_at'])
    return s


def tweets_to_df(tweets):
    """
    Takes list of Tweets in JSON format (dictionaries) and converts it to a Pandas DataFrame.
    
    Parameters
    ---------
    tweets: list of dictionaries
        Tweets in JSON format as returned by requests.get(...).json()
        
    Returns
    -------
    DataFrame
        Useful information extracted from each Tweet and compiled in a Pandas DataFrame
    """

    import numpy as np
    import pandas as pd
    
    df = pd.DataFrame()
    
    df['id'] = [tweet['id'] for tweet in tweets]
    df['user_name'] = [tweet['user']['name'] for tweet in tweets]
    df['user_screenname'] = [tweet['user']['screen_name'] for tweet in tweets]
    df['user_description'] = [tweet['user']['description'] for tweet in tweets]
    df['user_friends'] = [tweet['user']['friends_count'] for tweet in tweets]
    df['user_followers'] = [tweet['user']['followers_count'] for tweet in tweets]
    df['user_favorites'] = [tweet['user']['favourites_count'] for tweet in tweets]
    df['retweets'] = [tweet['retweet_count'] for tweet in tweets]
    df['date'] = [tweet['created_at'] for tweet in tweets]
    df['location'] = [tweet['user']['location'] if tweet['user']['location'] != '' \
                      else np.nan for tweet in tweets]
    df['geocode'] = [tweet['geo'] for tweet in tweets]
    df['hashtags'] = [[inner_dict['text'] for inner_dict in tweet['entities']['hashtags']] \
                      if tweet['entities']['hashtags'] != [] else np.nan for tweet in tweets]
    df['tweet'] = [tweet['text'].strip() for tweet in tweets]
    
    return df


def get_tweets_premium(api_connection, num_pages, product, label, query, fromDate, toDate, maxResults):
    """
    Queries tweets from the Twitter Premium APIs ('30-Day' and 'Full Archive') without exceeding the 
    Sandbox rate limits. Pages through the search results to avoid repeated queries and returns tweets 
    as a list of dictionaries (JSON format). Fails on error with status code output. 
    
    Parameters
    ---------
    api_connection: TwitterAPI object
        authenticated TwitterAPI connection for REST API or Streaming API access
    num_pages: int
        the number of search result pages to return (i.e. number of requests), subject to request limits
        total number of tweets returned will be approximately maxResults * num_pages
    product: string: '30day' or 'fullarchive'
        the Premium API to be accessed
        '30day' accesses tweets from the prior 30 days; 'fullarchive' accesses tweets from all years
        request limits apply: see https://developer.twitter.com/en/docs/tweets/search/overview/premium
    label: string
        the label of the 'dev environment' setup for Premium API access
    query: string
        the search query 
        see https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search for details
    fromDate: string
        oldest UTC timestamp to consider in search query (subject to API limitations)
        applies minute-level granularity (e.g. '201201010000')
    toDate: string
        most recent UTC timestamp to consider in search query (subject to API limitations)
        applies minute-level granularity
    maxResults: int
        maximum number of tweets returned per request/page
        total number of tweets returned will be approximately maxResults * num_pages
        request limits apply: Sandbox access grants maxResults of at most 100 tweets
        
    Returns
    -------
    list of dictionaries (or error status code)
        Queried tweets in JSON format
    """

    import time
    
    r = api_connection.request('tweets/search/{}/:{}'.format(product, label), 
                                {'query': query, 
                                 'fromDate': fromDate,
                                 'toDate': toDate,
                                 'maxResults': maxResults})
    
    if r.status_code != 200:
        print('status code: ' + str(r.status_code))
        # see https://developer.twitter.com/en/docs/basics/response-codes.html for details
        return    
    
    json = r.json()
    tweets = json['results']
    next_key = json['next']  # next key provided only if additional pages available
    
    page = 2
    
    while page <= num_pages:
        
        r = api_connection.request('tweets/search/{}/:{}'.format(product, label), 
                                    {'query': query, 
                                     'fromDate': fromDate,
                                     'toDate': toDate,
                                     'maxResults': maxResults,
                                     'next': next_key})  # requests tweets from the next page
        
        if r.status_code != 200:
            print('status code: ' + str(r.status_code))
            break
        
        json = r.json()
        tweets += json['results']  # combine with previous results
        
        if 'next' not in json:  # stop if no next_key provided (no further pages)
            break
        
        time.sleep(3)  # ensures compatibility with Sandbox rate limits
        next_key = json['next']
        page += 1
    
    return tweets


def tweets_db_to_df(collection, filters = {}):
    """
    Pull tweets from MongoDB database and compile them in Pandas DataFrame.
    
    Parameters
    ---------
    collection: pymongo.collection.Collection
        MongoDB collection containing tweets
    filters: dictionary, default: {}
        filters applied for tweet querying
        
    Returns
    -------
    DataFrame
        extracts ID, full tweet text, year, and location for each tweet and returns as row of DataFrame
    """
    
    import numpy as np
    import pandas as pd

    cursor = collection.find(filters, {'_id': 0})  # query the database
    new_list = []
    
    for tweet in cursor:
        new_dict = {}
        new_dict['ID'] = tweet['id']
        
        try:
            # get full tweet text if truncated
            new_dict['text'] = tweet['retweeted_status']['extended_tweet']['full_text']
        except:
            new_dict['text'] = tweet['text']
        
        new_dict['year'] = tweet['year']
        new_dict['location'] = tweet['user']['location']
        
        new_list.append(new_dict)
    
    df = pd.DataFrame(new_list)
    df['location'] = df['location'].replace({None: np.nan})  # handle missing locations
    return df

