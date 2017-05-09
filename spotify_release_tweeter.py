import pickle
from datetime import datetime
import os

import settings

import spotipy
import spotipy.util
from twython import Twython


class Tweeter(object):
    def __init__(self):
        self.twitter = Twython(settings.TWITTER_APP_KEY,
                               settings.TWITTER_APP_SECRET,
                               settings.TWITTER_OAUTH_TOKEN,
                               settings.TWITTER_OAUTH_TOKEN_SECRET)

    def tweet_list(self, status_list):
        for status in status_list:
            self.tweet(status)

    def tweet(self, status):
        self.twitter.update_status(status=status[:140])


class AlreadyHandledCache(object):
    def __init__(self, cache_path):
        self.cache_path = cache_path
        try:
            with open(self.cache_path, "rb") as out:
                self.cache = pickle.load(out)
        except FileNotFoundError:
            self.cache = []
        print("Loaded cache has {} entries.".format(len(self.cache)))

    def update(self, entries):
        self.cache.extend(entries)
        with open(self.cache_path, "wb") as out:
            pickle.dump(self.cache, out)

    def reduce(self, entries):
        reduced_list = list(set(entries) - set(self.cache))
        self.update(reduced_list)
        return reduced_list


class SpotifyRelease(object):
    def __init__(self, release_id, artists, title, release_type):
        self.release_id = release_id
        self.url = "https://play.spotify.com/album/{}".format(self.release_id)
        self.title = title
        self.release_type = release_type
        self.artist_name = artists[0]['name']

    def to_twitter_string(self):
        characters_left = 136 - len(self.url) - len(self.artist_name)
        title = self.title[:characters_left]
        return "{} - {} {}".format(self.artist_name, title, self.url)


def create_twitter_status_strings_from_releases_per_artist(releases_per_artist):
    result = list()
    for artist_id in releases_per_artist:
        for release in releases_per_artist[artist_id]:
            result.append(release.to_twitter_string())
    return result


def is_first_run():
    return not os.path.exists(settings.TWEETED_IDS_CACHE_PATH)


def item_to_spotify_release(item):
    return SpotifyRelease(release_id=item['id'],
                          artists=item['artists'],
                          title=item['name'],
                          release_type=item['album_type'])


class SpotifyReleaseTweeter(object):

    def __init__(self):
        token = spotipy.util.prompt_for_user_token(
            settings.SPOTIFY_USER_NAME,
            scope='user-follow-read',
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI)
        self.spotify = spotipy.Spotify(auth=token)
        self.is_first_run = is_first_run()
        self.cache = AlreadyHandledCache(settings.TWEETED_IDS_CACHE_PATH)
        self.process()

    def get_ids_of_followed_artists(self):
        result = list()
        last_artist_id = None

        while True:
            artist_result = self.spotify.current_user_followed_artists(50, last_artist_id)
            artists = artist_result['artists']['items']

            if not artists:
                break

            for artist in artists:
                last_artist_id = artist['id']
                result.append(artist['id'])

        print("{} followed artists found.".format(len(result)))
        return result

    def filter_releases(self, artist_releases):
        release_ids = [release.release_id for release in artist_releases]
        reduced_ids = self.cache.reduce(release_ids)
        filtered_releases = filter(lambda release: release.release_id in reduced_ids, artist_releases)
        return list(filtered_releases)

    def get_releases_per_artist(self, artist_ids, with_appearance=False, limit=settings.LAST_N_RELEASES):
        result = dict()

        for artist_id in artist_ids:
            result[artist_id] = list()
            artist_releases = list()

            # Albums
            result_albums = self.spotify.artist_albums(artist_id=artist_id, album_type='album',
                                                       country=settings.SPOTIFY_MARKET, limit=limit)
            albums = [item_to_spotify_release(item) for item in result_albums['items']]
            artist_releases.extend(albums)

            # Singles
            result_singles = self.spotify.artist_albums(artist_id=artist_id, album_type='single',
                                                        country=settings.SPOTIFY_MARKET, limit=limit)
            singles = [item_to_spotify_release(item) for item in result_singles['items']]
            artist_releases.extend(singles)

            # Appearances
            if with_appearance:
                result_appearances = self.spotify.artist_albums(artist_id=artist_id, album_type='appears_on',
                                                                country=settings.SPOTIFY_MARKET, limit=limit)
                appearances = [item_to_spotify_release(item) for item in result_appearances['items']]
                artist_releases.extend(appearances)

            # Filter
            filtered_releases = self.filter_releases(artist_releases)
            if filtered_releases:
                result[artist_id] = filtered_releases
        return result

    def process(self):
        print("Start ({}).".format(datetime.now()))
        artist_ids = self.get_ids_of_followed_artists()
        releases_per_artist = self.get_releases_per_artist(artist_ids)
        twitter_status_strings = create_twitter_status_strings_from_releases_per_artist(releases_per_artist)
        if not self.is_first_run:
            print("{} releases will be tweeted.".format(len(twitter_status_strings)))
            Tweeter().tweet_list(twitter_status_strings)
        else:
            print("Zero tweets at first run, due to Twython API limit (200 tweets a day). The cache is now initialized \
                  and the script will run as promised in the next run. All releases until now will not be tweeted \
                  anymore.")
        print("Done ({}).".format(datetime.now()))


if __name__ == '__main__':
    SpotifyReleaseTweeter()
