import pickle
from datetime import datetime

import settings
import util

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

    def update(self, entries):
        self.cache.extend(entries)
        with open(self.cache_path, "wb") as out:
            pickle.dump(self.cache, out)

    def reduce(self, entries):
        reduced_list = list(set(entries) - set(self.cache))
        self.update(reduced_list)
        return reduced_list


class SpotifyRelease(object):

    def __init__(self, release_id, artists, url, title, release_type, release_date):
        self.release_id = release_id
        self.artists = artists
        self.url = url
        self.title = title
        self.release_type = release_type
        self.release_date = release_date
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


def filter_releases(releases_per_artist):
    result = dict()
    last_update_date = datetime.strptime(util.get_last_update_date(), settings.DATE_FORMAT)

    for artist_id in releases_per_artist:
        result[artist_id] = list()
        for release in releases_per_artist[artist_id]:
            try:
                release_date = datetime.strptime(release.release_date, settings.DATE_FORMAT)
            except ValueError:
                release_date = datetime.strptime("{}-01-01".format(release.release_date), settings.DATE_FORMAT)
            if release_date >= last_update_date:
                result[artist_id].append(release)
    return result


class SpotifyReleaseTweeter(object):

    def __init__(self):
        token = spotipy.util.prompt_for_user_token(
            settings.SPOTIFY_USER_NAME,
            scope='user-follow-read',
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIFY_REDIRECT_URI
        )

        self.spotify = spotipy.Spotify(auth=token)
        self.process()
        util.save_last_update_date()

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

    def get_full_release(self, release_id):
        release = self.spotify.album(album_id=release_id)
        release_object = SpotifyRelease(release_id=release['id'],
                                        artists=release['artists'],
                                        release_type=release['type'],
                                        release_date=release['release_date'],
                                        title=release['name'],
                                        url=release['external_urls']['spotify'])

        print("Got full release info of {} - {}.".format(release_object.artist_name, release_object.title))
        return release_object

    def get_releases_per_artist(self, artist_ids, with_appearance=False, limit=settings.LAST_N_RELEASES):
        result = dict()

        for artist_id in artist_ids:
            result[artist_id] = list()
            artist_release_ids = set()

            # Albums
            result_albums = self.spotify.artist_albums(artist_id=artist_id, album_type='album',
                                                       country=settings.SPOTIFY_MARKET, limit=limit)
            artist_release_ids.update([album['id'] for album in result_albums['items']])

            # Singles
            result_singles = self.spotify.artist_albums(artist_id=artist_id, album_type='single',
                                                        country=settings.SPOTIFY_MARKET, limit=limit)
            artist_release_ids.update([single['id'] for single in result_singles['items']])

            # Appearances
            if with_appearance:
                result_appearances = self.spotify.artist_albums(artist_id=artist_id, album_type='appears_on',
                                                                country=settings.SPOTIFY_MARKET, limit=limit)
                artist_release_ids.update([appearance['id'] for appearance in result_appearances['items']])

            # Reduce release ids via already tweeted release ids cache
            cache = AlreadyHandledCache(settings.TWEETED_IDS_CACHE_PATH)
            for release_id in cache.reduce(artist_release_ids):
                result[artist_id].append(self.get_full_release(release_id))
        return result

    def process(self):
        print("Start ({}).".format(datetime.now()))
        artist_ids = self.get_ids_of_followed_artists()
        releases_per_artist = self.get_releases_per_artist(artist_ids)
        filtered_releases_per_artist = filter_releases(releases_per_artist)
        twitter_status_strings = create_twitter_status_strings_from_releases_per_artist(filtered_releases_per_artist)
        print("{} releases will be tweeted.".format(len(twitter_status_strings)))
        Tweeter().tweet_list(twitter_status_strings)
        print("Done ({}).".format(datetime.now()))
