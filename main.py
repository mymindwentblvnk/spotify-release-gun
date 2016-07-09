from spotipy_module import *
from config import *
from twitter_module import TwitterAdapter

user = User()
s = Spotify(user)
result = s.getAllNewReleases()

twitter = TwitterAdapter()
twitter.tweetList(result)