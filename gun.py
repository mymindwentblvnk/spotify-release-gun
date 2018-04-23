import requests
import json
from json.decoder import JSONDecodeError
from datetime import datetime
import os

import settings

from spotipy import Spotify
import spotipy.util
from requests.exceptions import ConnectionError


class AlreadyHandledCache(object):

    def __init__(self, cache_path):
        self.cache_key = 'already_handled_ids'
        self.cache_path = cache_path
        try:
            with open(cache_path, "r") as out:
                self.cache = json.load(out)[self.cache_key]
        except FileNotFoundError:
            self.cache = list()
        print("> Loaded cache has {} entries.".format(len(self.cache)))

    def update(self, entries):
        self.cache.extend(entries)
        with open(self.cache_path, "w") as out:
            cache_dict = {
                self.cache_key: self.cache
            }
            json.dump(cache_dict, out, indent=4)

    def reduce(self, entries):
        reduced_list = list(set(entries) - set(self.cache))
        self.update(reduced_list)
        return reduced_list


def is_first_run(cache_path):
    return not os.path.exists(cache_path)


def send_to_really_simple_rss_server(releases_per_artist, user_name):
    url = settings.REALLY_SIMPLE_RSS_SERVER_URL.format(user_name=user_name)
    for artist_id in releases_per_artist:
        for release in releases_per_artist[artist_id]:
            artists = ', '.join(release.artist_names)
            release_dict = {
                'days_valid': 90,
                'link': release.url,
                'title': '{} - {} [{}, ({})]'.format(artists,
                                                     release.title,
                                                     release.release_type,
                                                     release.release_date)
            }
            requests.post(url, json=release_dict)


def send_to_slack(releases_per_artist, user_name):
    pattern = '{} - {} [{} ({})]: {}'
    messages = []
    for artist_id in releases_per_artist:
        for release in releases_per_artist[artist_id]:
            artists = ', '.join(release.artist_names)
            message = pattern.format(artists,
                                     release.title,
                                     release.release_type,
                                     release.release_date,
                                     release.url)
            messages.append(message)
    requests.post(settings.SLACK_URL, json={'text': '\n'.join(messages)})
    return messages


class SpotifyRelease(object):

    def __init__(self, data):
        self.release_id = data['id']
        self.url = "https://play.spotify.com/album/{}".format(data['id'])
        self.title = data['name']
        self.artist_names = [a['name'] for a in data['artists']]
        self.release_type = data['album_group'].capitalize()
        self.release_date = data['release_date']


class SpotifyReleaseGun(object):

    def __init__(self, spotify_user_data):
        self.user_name = spotify_user_data['user_name']
        token = spotipy.util.prompt_for_user_token(
            self.user_name,
            scope='user-follow-read',
            client_id=spotify_user_data['client_id'],
            client_secret=spotify_user_data['client_secret'],
            redirect_uri=spotify_user_data['redirect_uri']
        )
        self.spotify = Spotify(auth=token)
        self.cache_path = settings.CACHE_PATH_PATTERN.format(self.user_name)
        self.is_first_run = is_first_run(self.cache_path)
        self.cache = AlreadyHandledCache(self.cache_path)

    def get_ids_of_followed_artists(self):
        result = []
        last_artist_id = None

        while True:
            artist_result = self.spotify.\
                current_user_followed_artists(50, last_artist_id)
            if artist_result['artists']['items']:
                for artist in artist_result['artists']['items']:
                    last_artist_id = artist['id']
                    result.append(artist['id'])
        return result

    def filter_releases(self, artist_releases):
        release_ids = [release.release_id for release in artist_releases]
        reduced_ids = self.cache.reduce(release_ids)
        filtered = filter(
            lambda release: release.release_id in reduced_ids, artist_releases
        )
        return list(filtered)

    def get_releases_per_artist(self,
                                artist_ids,
                                limit=settings.LAST_N_RELEASES):
        releases_per_artist_id = {}

        for artist_id in artist_ids:
            artist_releases = []
            try:
                # Albums
                result_albums = self.spotify.artist_albums(
                    artist_id=artist_id,
                    album_type='Album',
                    country=settings.SPOTIFY_MARKET,
                    limit=limit
                )
                albums = [SpotifyRelease(d) for d in result_albums['items']]
                artist_releases.extend(albums)
                # Singles
                result_singles = self.spotify.artist_albums(
                    artist_id=artist_id,
                    album_type='Single',
                    country=settings.SPOTIFY_MARKET,
                    limit=limit
                )
                singles = [SpotifyRelease(d) for d in result_singles['items']]
                artist_releases.extend(singles)
            except ConnectionError:
                print(("> Could not establish connection while "
                       "fetching singles for artist with id {}. "
                       "Skipping.").format(artist_id))
            except JSONDecodeError:
                print(("> Could not decode JSON response "
                       "of artist with id {}. Skipping.").format(artist_id))

            filtered_releases = self.filter_releases(artist_releases)
            if filtered_releases:
                releases_per_artist_id[artist_id] = filtered_releases
        return releases_per_artist_id

    def get_releases_of_artists(self):
        artist_ids = self.get_ids_of_followed_artists()
        print("> {} followed artists found.".format(len(artist_ids)))
        releases_per_artist = self.get_releases_per_artist(artist_ids)
        return releases_per_artist

    def process(self):
        print("> Start ({}).".format(datetime.now()))
        releases = self.get_releases_of_artists()
        if settings.REALLY_SIMPLE_RSS_SERVER_URL:
            send_to_really_simple_rss_server(releases, self.user_name)
        if settings.SLACK_URL:
            send_to_slack(releases, self.user_name)
        print("> Done ({}).".format(datetime.now()))


if __name__ == '__main__':
    for user_name, user_data in settings.SPOTIFY_USERS.items():
        print("Processing Spotify user", user_name)
        s = SpotifyReleaseGun(user_data)
        s.process()
