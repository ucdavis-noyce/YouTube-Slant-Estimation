import subprocess
import db
import json
from random import choice
import requests
import os

def get_automatic_captions(js):
    captions = js.get('automatic_captions', {})
    if 'en' not in captions:
        return None
    return captions['en'][0]['url']

def get_subtitles(js):
    subtitles = js.get('subtitles', {})
    if 'en' not in subtitles:
        return None
    return subtitles['en'][0]['url']

def get_metadata(videoId):

    # search for metadata in db
    metadata_in_db = db.get_metadata(videoId)
    if metadata_in_db is not None:
        return metadata_in_db

    url = 'https://youtube.com/watch?v=%s' % videoId

    try:
        js = json.loads(subprocess.run(['youtube-dl', '-J', url], stdout=subprocess.PIPE).stdout)
    except:
        return None
        
    metadata = dict(
        video_id=videoId,
        title=js.get('title', ''),
        thumbnail=js.get('thumbnail'),
        description=js.get('description', ''),
        upload_date=js.get('upload_date', ''),
        uploader=js.get('uploader', ''),
        channel_id=js.get('channel_id', ''),
        duration=js.get('duration', ''),
        view_count=js.get('view_count', ''),
        like_count=js.get('like_count', ''),
        average_rating=js.get('average_rating', ''),
        categories=','.join(js.get('categories', [])),
        subtitles=get_subtitles(js),
        automated_captions=get_automatic_captions(js)
    )

    db.save_to_db('video-metadata', metadata)

    return metadata

def get_api_key():
    with open('data/youtube-tokens.txt') as fp:
        return choice(fp.read().strip().split('\n'))
         
def get_comment_threads(videoId, pages=5, maxResults=100):
    nextPageToken = ''
    comments = []
    api_key = get_api_key()
    for _ in range(pages):
        # params for request
        params = {
            'key': api_key,
            'textFormat': 'plainText',
            'part': 'snippet,replies',
            'videoId': videoId,
            'maxResults': maxResults,
            'pageToken': nextPageToken
        }
        
        # send request to API
        r = requests.get('https://www.googleapis.com/youtube/v3/commentThreads', params=params)
        js = r.json()

        if 'error' in js:
            raise Exception(js['error']['message'])

        comments.append(js)
                
        # check if next page exists, else break
        if 'nextPageToken' not in js:
            break

        # setup for next call
        nextPageToken = js['nextPageToken']
    return comments

def parse_comment(comment):
    return dict(
        video_id = comment['snippet']['videoId'],
        comment_id = comment['id'],
        author_id = comment['snippet']['authorChannelId']['value'],
        author_name = comment['snippet']['authorDisplayName'],
        comment = comment['snippet']['textOriginal'],
        parent_id = comment['snippet'].get('parentId', None),
        published_at = comment['snippet']['publishedAt'],
        likes = comment['snippet']['likeCount']
    )

def get_parsed_comments(videoUrl, pages=5, maxResults=100):
    results = get_comment_threads(videoUrl, pages, maxResults)
    comments = []
    # parse each page response
    for page in results:
        threads = page.get('items', [])
        for thread in threads:
            # get root comment and replies
            topLevelComment = thread['snippet']['topLevelComment']
            if 'replies' in thread:
                replies = thread['replies']['comments']
            else:
                replies = []
            # save comment and replies
            comments.append(topLevelComment)
            comments.extend(replies)

    # send parsed comments in response
    for c in comments:
        try:
            yield parse_comment(c)
        except:
            pass

def get_comments(videoId):

    # search for metadata in db
    comments_in_db = db.get_comments(videoId)
    if comments_in_db is not None:
        return {'video_id': videoId, 'comments': comments_in_db}

    comments = []
    try:
        for comment in get_parsed_comments(videoId):
            comments.append(comment)
        db.save_to_db('comments', comments)
        return {'video_id': videoId, 'comments': comments}
    except Exception as e:
        return {'error': True, 'description': str(e)}
