# SpotifyNotificationTweeter
A Python 3.5 script that tweets about new releases of artists that you follow.

## What it does 
1. Logs on to your Spotify account (via Web-API [https://developer.spotify.com/web-api/](https://developer.spotify.com/web-api/) using [Spotipy](https://spotipy.readthedocs.io/en/latest/)).
2. Gets all your followed artists.
3. Gets for all those artists the latest _n_ albums, singles or appearances.
4. Checks if there are new albums for an artist since the last time it checked (last update is saved in an external file).
5. Tweets about all new releases since the last update (using [Twython](https://twython.readthedocs.io/en/latest/)).

## If you want to use it
1. Clone/download repository.
2. Use Python 3.5.
3. Install missing python modules ([Twython](https://twython.readthedocs.io/en/latest/) and [Spotipy](https://spotipy.readthedocs.io/en/latest/)).
4. Rename `rename_to_config.py` to `config.py` and enter the missing API information (Twitter and Spotify).
5. Run `main.py` with Python 3.5.

## Run it daily on your Raspberry Pi
6. Install git on your Pi and follow the steps above (_If you want to use it_). 
7. Run the script once manually, so the Spotipy cache can be generated.
8. Now we define a cronjob (https://www.raspberrypi.org/documentation/linux/usage/cron.md) and schedule the script every night.
  1. Open the terminal (`STRG + ALT + T`)
  2. `crontab -e`
  3. And make this entry: `0 1 * * * cd /home/pi/scripts/SpotifyNotificationTweeter/ && python3.4 main.py > /home/pi/logs/snt.log`. The `cd`command was necessary for me, because otherwise the cronjob cannot find the Spotipy cache.
  4. Save and close.
9. The SpotifyNotificationTweeter will now run every night at 1 AM. 

## Is using
* Spotipy [http://spotipy.readthedocs.io/en/latest/](https://spotipy.readthedocs.io/en/latest/)
* Twython [https://twython.readthedocs.io/en/latest/](https://twython.readthedocs.io/en/latest/)

## Todo
* Log to a file.
* Log to a file and put it in Dropbox (via Dropbox API)
