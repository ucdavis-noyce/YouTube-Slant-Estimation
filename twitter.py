import db
import json
import requests
from random import choice

with open('data/tokens.txt') as tokens:
    bearer_tokens = tokens.read().strip().split('\n')

def get_tweets(q):
    # search for tweets in db
    tweets_in_db = db.get_tweets(q)
    if tweets_in_db is not None:
        return tweets_in_db

    # tweets not found, use twitter api
    bearer_token = choice(bearer_tokens)
    search_url = "https://api.twitter.com/2/tweets/search/all"
    query_params = {'query': f'url:"{q}"', 'tweet.fields': 'id,text', 'expansions': 'author_id', 'user.fields': 'id,name,username', 'max_results': 100, 'start_time': '2006-12-31T23:59:59.999Z'}
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    res = requests.get(search_url, headers=headers, params=query_params)
    js = res.json()

    if 'meta' not in js:
        raise Exception('Issue with API')
        
    # save found tweets to db
    if js['meta']['result_count'] > 0:
        db.save_to_db('slant-tweets', {'query': q, 'tweets': json.dumps(js)})
        
    return js
