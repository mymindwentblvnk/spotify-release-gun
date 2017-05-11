[![Build
Status](https://travis-ci.org/michael-123/SpotifyReleaseTweeter.svg?branch=master)](https://travis-ci.org/michael-123/SpotifyReleaseTweeter)

# SpotifyReleaseTweeter
A Python tool that tweets about new releases of artists that you follow.

## What it does 
1. Logs on to your Spotify account.
2. Gets all your followed artists.
3. Gets for all those artists the latest _n_ albums, singles or appearances.
4. Checks if there are new releases for an artist (check against a cache of already handled releases).
5. Tweets about all new releases since the last update.

## If you want to use it
1. Clone repository.
2. Create virtualenv ```sudo virtualenv -p python3 venv```
3. ```pip install -r requirements.txt```
4. Rename `rename_to_settings.py` to `settings.py` and enter the missing API information.
5. Run ```python spotify_release_tweeter.py```
