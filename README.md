# SpotifyNotificationTweeter
A Python 3.5 script that tweets about new releases of artists that you follow.

## What it does 
1. Logs on to your Spotify account (via Web-API [https://developer.spotify.com/web-api/](https://developer.spotify.com/web-api/) using [spotipy](https://spotipy.readthedocs.io/en/latest/)).
2. Gets all your followed artists.
3. Gets for all those artists the latest n albums, singles or appearances.
4. Checks if there are new albums for an artist since the last time it checked (last update is saved in an external file).
5. Tweets about all new releases since the last update (using [Twython](https://twython.readthedocs.io/en/latest/)).

## If you want to use it
1. Clone/download repository.
2. Use Python 3.5.
3. Install missing python modules ([Twython](https://twython.readthedocs.io/en/latest/) and [spotipy](https://spotipy.readthedocs.io/en/latest/)).
4. Rename `rename_to_config.py` to `config.py` and enter the missing API information (Twitter and Spotify).
5. Run `main.py` with Python 3.5.

## Is using
* spotipy [http://spotipy.readthedocs.io/en/latest/](https://spotipy.readthedocs.io/en/latest/)
* Twython [https://twython.readthedocs.io/en/latest/](https://twython.readthedocs.io/en/latest/)

## Todo
* Log to a file.
* Log to a file and put it in Dropbox (via Dropbox API)
* Tutorial on how to run the script on a Raspberry Pi with [crontab](https://www.raspberrypi.org/documentation/linux/usage/cron.md)
