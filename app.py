from flask import Flask
from flask_cors import CORS, cross_origin
import json
import twitter
import slant
import youtube


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/getTweets/<query>")
@cross_origin()
def get_tweets(query):
    return json.dumps(twitter.get_tweets(query))

@app.route("/getSlant/<query>")
@cross_origin()
def get_slant(query):
    response = slant.get_slant_score(query)
    response_code = 200
    if response.get('error', False):
        response_code = 404
    return json.dumps(response), response_code

@app.route("/getMetadata/<query>")
@cross_origin()
def get_metadata(query):
    response = youtube.get_metadata(query)
    response_code = 200
    if response.get('error', False):
        response_code = 404
    return json.dumps(response), response_code


@app.route("/getComments/<query>")
@cross_origin()
def get_comments(query):
    response = youtube.get_comments(query)
    response_code = 200
    if response.get('error', False):
        response_code = 404
    return json.dumps(response), response_code

@app.route("/")
def main():
    return "<p>YouTube Audit API</p>"
