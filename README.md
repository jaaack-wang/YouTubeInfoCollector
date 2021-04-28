# YouTubeInfoCollector
These 6 casual Python scripts were written last year, which can help one easily scrape data from YouTube website. These scripts can be thus ultilized to compile corpora of YouTube video titles and comments. The compiled corpora will also contain view counts, counts of likes and dislikes, date etc., which is good for sentiment analysis. 

## Requirements
- Python: 3.5 or later.
- Other packages: [pandas](https://pandas.pydata.org), [requests](https://pypi.org/project/requests/), [BeautifulSoup](https://pypi.org/project/beautifulsoup4/), [selenium](https://github.com/SeleniumHQ/selenium/tree/trunk/py) and a [driver](https://github.com/SeleniumHQ/selenium/tree/trunk/py#drivers) for selenium 

## How to use
Please download these scripts and use them directly. The functionalities of these scripts are described below:

- [search.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/search.py): Given a query, this script will output an excel file that details a list of videos related to the query: title, post date, view count, like count, dislike count and a link to the video.
- [channel.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/channel.py): Given a link to a YouTube Channel's "VIDEOS" webpage, the script will output an excel file that contains the above information of videos on that Channel. 
- [comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/comments.py): Given a lin to a YouTube video, the script will output an excel file that contains comments (along with username, post date, upvote cont) posted for that video. The general info of the video, i.e., view count, like count, dislike count and the link, is also included. 
- [search_comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/search_comments.py): Given a query, the script will output an excel file as `search.py` and a list of excel files returned by `comments.py` for all the videos captured by `search.py`.
- [channel_comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/channel_comments.py): Given a link to a YouTube Channel's "VIDEOS" webpage, the script will output excel files that result from both `channel.py` and `comments.py`.
- [search_channel_comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/search_channel_comments.py): Given a query, the script will find all the YouTube channels for the captured videos and then scrape comments from the comments posted for the videos on those channels. 

Please note that, the scripts above also allow for entires of multiple queries or comments at once. 
