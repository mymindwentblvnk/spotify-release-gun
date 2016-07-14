from spotify_module import *
from config import *
from twitter_module import TwitterAdapter
from util import save_last_update


def tweet_new_releases():
    user = SpotifyUser()
    s = Spotify(user)
    result = s.get_all_new_releases()

    user = TwitterUser()
    twitter = TwitterAdapter(user)
    twitter.tweet_list(result)

    # LOGGING
    print("%s Tweet(s) sent." % (len(result)))

    # Save date
    save_last_update()
