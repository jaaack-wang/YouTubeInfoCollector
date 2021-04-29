# YouTubeInfoCollector
These 6 casual Python scripts were written last year, which can help one easily scrape data from YouTube website. These scripts can be thus ultilized to compile
information such as video titles, post dates, view counts, like/dislike counts, and comments together as a corpus. The corpus is good for sentiment analysis because it contains some direct indicators for sentiments (i.e., like/dislike). One can also use the information collected to analyze a YouTube channel, a specific topic discussed on YouTube etc. 

## Requirements
- Python: 3.5 or later.
- Other packages: [pandas](https://pandas.pydata.org), [requests](https://pypi.org/project/requests/), [BeautifulSoup](https://pypi.org/project/beautifulsoup4/), [selenium](https://github.com/SeleniumHQ/selenium/tree/trunk/py) and a [driver](https://github.com/SeleniumHQ/selenium/tree/trunk/py#drivers) for selenium 

## How to use
Please download these scripts and use them directly. The functionalities of these scripts are described below. Please note that, the scripts all allow entries of multiples queries or links, but for simplity, I only discuss the situation of a single query or link.

- [search.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/search.py): Given a query, this script will output an excel file that details a list of videos related to the query: titles, post dates, view counts, like counts, dislike counts and links to these videos.
- [channel.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/channel.py): Given a link to a YouTube Channel's "VIDEOS" webpage, the script will output an excel file that contains the above information for videos posted on that Channel. 
- [comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/comments.py): Given a link to a YouTube video, the script will output an excel file that contains comments (along with usernames, post dates, upvote conts) posted for that video. The general info of the video, i.e., view count, like count, dislike count and the link, is also included. 
- [search_comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/search_comments.py): Given a query, the script will output an excel file as `search.py` and a list of excel files returned by `comments.py` for all the videos captured by `search.py`.
- [channel_comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/channel_comments.py): Given a link to a YouTube Channel's "VIDEOS" webpage, the script will output excel files that result from both `channel.py` and `comments.py`.
- [search_channel_comments.py](https://github.com/jaaack-wang/YouTubeInfoCollector/blob/main/YouTube_Info_Collector/search_channel_comments.py): Given a query, the script will find all the YouTube channels for the captured videos and then scrape comments from the comments posted for the videos on those channels. 

