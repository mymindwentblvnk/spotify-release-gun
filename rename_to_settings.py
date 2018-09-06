SPOTIFY_MARKET = '<country_code>'
LAST_N_RELEASES = 10

# https://developer.spotify.com/my-applications/#!/applications
SPOTIFY_USERS = {
    '<user_name>': {
            'client_id': '<client_id>',
            'client_secret': '<client_secret>',
            'redirect_uri': '<redirect_uri>',
            'user_name': '<user_name>',
    },
    # ...
}

CACHE_PATH_PATTERN = '.already-notified-{}'


REALLY_SIMPLE_RSS_SERVER_URL = '<rsrs_url>/feed/spotify_releases/{user_name}'
SLACK_URL = '<slack_webhook_url>'
