# youtube-search-results API
This is a RESTful API made in Flask to extract video information available on youtube, without using Google's YouTube Data V3 API.

### This is the Version 4 of search-results api.
- Now supports caching, via mongodb Database.
- Better scarpping logic over the 'website'.
- Added Exception

# How to try

To use the API make a call to <code>https://search-results-api.herokuapp.com/youtube/QUERY</code>

where <code>QUERY</code>is the keyword you wish to get info of, separated by '+'. 

For eg: <code>https://search-results-api.herokuapp.com/youtube/alone+alan+walker</code>