from spotify_module import *
from config import *
from twitter_module import TwitterAdapter
from util import saveLastUpdate

def tweetNewReleases():
    user = SpotifyUser()
    s = Spotify(user)
    result = s.getAllNewReleases()

    user = TwitterUser()
    twitter = TwitterAdapter(user)
    twitter.tweetList(result)

    # LOGGING
    print("%s Tweets sent." % (len(result)))

    # Save date
    saveLastUpdate()