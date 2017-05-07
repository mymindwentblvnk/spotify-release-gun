# SpotifyReleaseTweeter
A Python 3.5 script that tweets about new releases of artists that you follow.

## What it does 
1. Logs on to your Spotify account.
2. Gets all your followed artists.
3. Gets for all those artists the latest _n_ albums, singles or appearances.
4. Checks if there are new albums for an artist since the last time it checked (last update is saved in an external file).
5. Tweets about all new releases since the last update.

## If you want to use it
1. Clone repository.
2. Create virtualenv ```sudo virtualenv -p python3 venv```
3. ```pip install -r requirements.txt```
4. Rename `rename_to_settings.py` to `settings.py` and enter the missing API information.
5. Run ```python main.py```

## TODO 
1. Tests
