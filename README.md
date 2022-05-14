# YouTube-Slant-Estimation
Simple web-server for collecting tweets, metadata, and comments for YouTube videos and estimating their slant based on the approach used in our audit of YouTube's recommendations. Read more about it [here](https://youtubeaudit.com). The server caches responses inside _data/database.db_ so as to avoid rate limits on the used APIs.

## Getting Started
1. Clone the repository.
2. Generate your [Twitter v2](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens) and [YouTube API tokens](https://developers.google.com/youtube/v3).
3. Copy the Twitter tokens to _data/twitter-tokens.txt_ and the YouTube tokens to _data/youtube-tokens.txt_ respectively, one per line.
4. Download [youtube-dl](https://youtube-dl.org/) to a location in your PATH.
5. For slant estimation, download the `landmark-counts.tar.xz` by filling out this [form](https://docs.google.com/forms/d/e/1FAIpQLSdsLGpK_p3OigqVODPkM7czYLtbj0oGgzBqx2PxOJNJCIWqjA/viewform?usp=sf_link) and extracting its contents to the _data_ directory.
6. Install the requirements using `pip install -r requirements.txt` inside the repository.
7. Start the server using `flask run --port 5000`.

## Usage
Consider the following URL: `https://www.youtube.com/watch?v=XpeOIww_l4A`. The part of the URL after the `watch?v=` is the video ID. The various endpoints of the server take this video ID and return the corresponding data. For example, to get the metadata for this video, you can use cURL as follows: `curl http://localhost:5000/getMetadata/XpeOIww_l4A`

## API Endpoints
- `/getMetadata/<video-id>`: Get video metadata using `youtube-dl`.
- `/getTweets/<video-id>`: Get tweets mentioning the video using the Twitter API.
- `/getComments/<video-id>`: Get comments on the video using the YouTube API.
- `/getSlant/<video-id>`: Get the estimated slant for the video using our approach.


## Acknowledgements
This tool was developed as part of an effort by researchers at UC Davis to audit the recommendations on YouTube. Read more about it [here](https://youtubeaudit.com).

The primary maintainer is [Muhammad Haroon](https://github.com/haroon96).
