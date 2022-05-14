# Tweet/Slant API

## Setting up:
- Download landmark cache from [here](https://drive.google.com/drive/folders/1jw9vpo_Mjg_Pe-ZtP_wdt4RZfsgWhPaS?usp=sharing) and paste it inside a folder called `cache`.
- Run using `flask run --port=XXXX`.

## Description:
API-implementation for Henry and Steve's slant estimation implementation that also caches results for repeated queries to both tweets and slant calculation.

## End-point Reference:
- `rostam.idav.ucdavis.edu/noyce/getTweets/<query>`: Get tweets for a certain query
- `rostam.idav.ucdavis.edu/noyce/getSlant/<query>`: Get slant score for a certain query

## Tips:
- For YouTube videos, results are most accurate when you just use the videoId. For example, to search tweets or get slant score for the video `https://www.youtube.com/watch?v=W5jWmeCZzp4`, visit `http://rostam.idav.ucdavis.edu/noyce/getSlant/W5jWmeCZzp4`
