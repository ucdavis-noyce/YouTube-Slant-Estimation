from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
import json
import pandas as pd

engine = create_engine('sqlite:///data/database.db')

def get_engine():
    return engine

def get_tweets(q):
    try:
        df = pd.read_sql('SELECT * FROM `twitter-api` WHERE query = "%s"' % q, con=get_engine())
        return None if df.empty else json.loads(df['tweets'].iloc[0])
    except OperationalError:
        return None

def get_channel_slant_score(channel_id):
    try:
        sql = 'SELECT slant FROM `video-metadata` vm JOIN `slant-scores` ss ON vm.video_id = ss.query WHERE channel_id = "%s"' % channel_id
        df = pd.read_sql(sql, con=get_engine())
        return None if df.empty else df['slant']
    except OperationalError:
        return None

def get_slant_score(q):
    try:
        df = pd.read_sql('SELECT * FROM `slant-scores` WHERE query = "%s"' % q, con=get_engine())
        return None if df.empty else df.iloc[0].to_dict()
    except OperationalError:
        return None


def get_metadata(videoId):
    try:
        df = pd.read_sql('SELECT * FROM `video-metadata` WHERE video_id = "%s"' % videoId, con=get_engine())
        return None if df.empty else df.iloc[0].to_dict()
    except OperationalError:
        return None


def get_comments(videoId):
    try:
        df = pd.read_sql('SELECT * FROM `comments` WHERE video_id = "%s"' % videoId, con=get_engine())
        return None if df.empty else df.to_dict(orient='records')
    except OperationalError:
        return None


def save_to_db(table, obj):
    if type(obj) == list:
        pd.DataFrame(obj).to_sql(table, index=False, con=get_engine(), if_exists='append')
    else:
        pd.DataFrame([obj]).to_sql(table, index=False, con=get_engine(), if_exists='append')
