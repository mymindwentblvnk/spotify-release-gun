# Please rename this file to config.py and add the API information below
# (Twitter and Spotify)


class SpotifyUser():
    """
    Spotify user information.
    """
    SPOTIFY_MARKET = "DE"
    NUMBER_OF_RELEASES_TO_LOOK_IN = 10
    # To receive following information visit
    # https://developer.spotify.com/my-applications/#!/applications
    # and register your application
    SPOTIFY_CLIENT_ID = ""
    SPOTIFY_CLIENT_SECRET = ""
    SPOTIFY_REDIRECT_URI = ""
    SPOTIFY_USER_NAME = ""

class TwitterUser():
    """
    Twitter user information.
    """
    # To receive following information visit https://dev.twitter.com/apps
    # and register your application
    APP_KEY = ""
    APP_SECRET = ""
    OAUTH_TOKEN = ""
    OAUTH_TOKEN_SECRET = ""


# Path to last update file
LAST_UPDATE_PATH = ".last_update_date"
# Path to the twitter_cache file
SPOTIFY_CACHE_PATH = ".twitter_cache"
# Turn logging on/off
LOGGING_ON = True