# spotify-release-gun
A Python tool that notifies about new releases of artists that you follow.

## What it does 
1. Logs on to your Spotify account.
2. Gets all your followed artists.
3. Gets for all those artists the latest _n_ albums, singles or appearances.
4. Checks if there are new releases for an artist (check against a cache of already handled releases).
5. Notifies about all new releases since the last update on
    * Slack via webhooks
    * [Really Simple RSS Server](https://github.com/mymindwentblvnk/really-simple-rss-server)

## If you want to use it
1. Clone repository.
2. Create virtualenv ```make venv```
4. Rename `rename_to_settings.py` to `settings.py` and enter the missing information.
5. Run ```make run```
