from twitter import get_tweets
import db
import pandas as pd
from youtube import get_metadata

landmark_counts = pd.read_pickle('data/landmark-counts.pkl')

def get_tweet_authors(q):
    tweets = get_tweets(q)
    if 'includes' in tweets and 'users' in tweets['includes']:
        users = tweets['includes']['users']
        return [u['username'].lower() for u in users]
    return []

def get_landmark_count(counts, landmark_type):
    try:
        return counts.loc[landmark_type]['count'].astype(int)
    except KeyError as _:
        return 0

def find_followed_landmarks(author):
    try:
        counts = landmark_counts.loc[author]
        return get_landmark_count(counts, 'c'), get_landmark_count(counts, 'l')
    except KeyError as _:
        return 0, 0

def get_channel_slant(videoId):
    try:
        metadata = get_metadata(videoId)
        channelId = metadata['channel_id']
        channel_slant = db.get_channel_slant_score(channelId)
    except:
        return {'error': True, 'description': 'Error with youtube-dl!', 'slant': None}
    if channel_slant is None:
        return {'error': True, 'description': 'Could not determine channel slant!', 'slant': None, 'channelId': channelId}
    return {'channel_id': channelId, 'mean_slant': channel_slant.mean(), 'median_slant': channel_slant.median()}

def get_slant_score(q):
    # search for slant in db
    slant_in_db = db.get_slant_score(q)
    if slant_in_db is not None:
        slant_in_db['cached'] = True
        return slant_in_db

    # slant not found in db, calculate it
    tweet_authors = get_tweet_authors(q)

    if len(tweet_authors) == 0:
        return {'error': True, 'description': 'Tweets not found!', 'slant': None, 'query': q}

    c, l = 0.0, 0.0
    for author in tweet_authors:
        conservative_landmarks, liberal_landmarks = find_followed_landmarks(author)
        c += conservative_landmarks
        l += liberal_landmarks
    
    if c == 0.0 and l == 0.0:
        return {'error': True, 'description': 'Tweets found but could not map landmarks!', 'slant': None, 'query': q}
        
    if c + l < 12:
        return {'error': True, 'description': 'Tweets found but not enough landmarks!', 'slant': None, 'query': q}

    response = {
        'slant': (c - l) / (c + l),
        'query': q,
        'conservative_landmark_follows': c,
        'liberal_landmark_follows': l
    }

    db.save_to_db('slant-scores', response)

    return response

