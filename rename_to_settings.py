SPOTIFY_MARKET = 'DE'
LAST_N_RELEASES = 10

# To receive following information visit
# https://developer.spotify.com/my-applications/#!/applications
# and register your application
SPOTIFY_USERS = {
    '<spotify_user_name>': {
        'client_id': '<client_id>',
        'client_secret': '<client_secret>',
        'redirect_uri': '<redirect_uri>',
        'user_name': '<spotify_user_name>',
    },
    # ...
}

NOTIFIED_IDS_CACHE_PATH_PATTERN = '.already-notified-{}'
