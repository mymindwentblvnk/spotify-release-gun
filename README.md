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
4. Rename `rename_to_settings.py` to `settings.py` and enter the missing information.
5. Run ```make docker-build-and-run```

### First time run

#### Authorize application
While your first run you are asked to authorize spotify-release-gun in your Spotify account so it can access your followed artists.
The prompt will look like this:

```
Processing Spotify user <your_user_name>


            User authentication requires interaction with your
            web browser. Once you enter your credentials and
            give authorization, you will be redirected to
            a url.  Paste that url you were directed to to
            complete the authorization.

        
Opened https://accounts.spotify.com/authorize?redirect_uri=<your_redirect_uri>&response_type=code&client_id=<client_id>&scope=user-follow-read in your browser


Enter the URL you were redirected to:

```

Open the link in your browser, authorize the application and you will be redirected to the redirect URI. Copy the URL and paste it into the terminal. This will generate the `.cache_<your_user_name>` file in the project folder. The next time you run the script everything works out as you'd wish for.

#### FYI

The first run will not generate notifications in [Really Simple RSS Server](https://github.com/mymindwentblvnk/really-simple-rss-server) or Slack since this run is there to build the cache file. Second run is the one that produces output.
