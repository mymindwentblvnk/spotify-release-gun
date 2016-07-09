from spotipy_module import *
from config import *
from twitter_module import TwitterAdapter

def tweetNewReleases():
    user = SpotifyUser()
    s = Spotify(user)
    result = s.getAllNewReleases()

    user = TwitterUser()
    twitter = TwitterAdapter(user)
    twitter.tweetList(result)