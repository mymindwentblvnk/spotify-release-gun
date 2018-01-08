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
        except UnicodeDecodeError:  # Cache still in pickle format
            import pickle
            with open(cache_path, "rb") as out:
                self.cache = pickle.load(out)
        print("> Loaded cache has {} entries.".format(len(self.cache)))

    def update(self, entries):
        self.cache.extend(entries)
        with open(self.cache_path, "w") as out:
            cache_dict = {
                self.cache_key: self.cache
            }
            json.dump(cache_dict, out)

    def reduce(self, entries):
        reduced_list = list(set(entries) - set(self.cache))
        self.update(reduced_list)
        return reduced_list


class SpotifyRelease(object):

    def __init__(self, release_id, artists, title, release_type):
        self.release_id = release_id
        self.url = "https://play.spotify.com/album/{}".format(self.release_id)
        self.title = title
        self.artist_name = artists[0]['name']
        self.release_type = release_type

    def to_twitter_string(self):
        pattern = "{} - {} ({}) {}"
        characters_left = 140 - len(pattern.replace('{}', '')) - len(self.url) - len(self.artist_name) - len(self.release_type)
        title = self.title[:characters_left]
        return pattern.format(self.artist_name, title, self.release_type, self.url)


def create_twitter_status_strings_from_releases_per_artist(releases_per_artist):
    result = list()
    for artist_id in releases_per_artist:
        for release in releases_per_artist[artist_id]:
            result.append(release.to_twitter_string())
    return result


def is_first_run(cache_path):
    return not os.path.exists(cache_path)


def item_to_spotify_release(item, release_type):
    return SpotifyRelease(release_id=item['id'],
                          artists=item['artists'],
                          title=item['name'],
                          release_type=release_type)


class SpotifyReleaseGun(object):

    def __init__(self, spotify_user_data):
        self.user_name = spotify_user_data['user_name']
        token = spotipy.util.prompt_for_user_token(self.user_name,
                                                   scope='user-follow-read',
                                                   client_id=spotify_user_data['client_id'],
                                                   client_secret=spotify_user_data['client_secret'],
                                                   redirect_uri=spotify_user_data['redirect_uri'])
        self.spotify = Spotify(auth=token)
        self.cache_path = settings.NOTIFIED_IDS_CACHE_PATH_PATTERN.format(self.user_name)
        self.is_first_run = is_first_run(self.cache_path)
        self.cache = AlreadyHandledCache(self.cache_path)

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

        print("> {} followed artists found.".format(len(result)))
        return result

    def filter_releases(self, artist_releases):
        release_ids = [release.release_id for release in artist_releases]
        reduced_ids = self.cache.reduce(release_ids)
        filtered_releases = filter(lambda release: release.release_id in reduced_ids, artist_releases)
        return list(filtered_releases)

    def get_releases_per_artist(self, artist_ids, limit=settings.LAST_N_RELEASES):
        ALBUM = 'Album'
        SINGLE = 'Single'
        result = dict()

        for artist_id in artist_ids:
            artist_releases = list()

            # Albums
            try:
                result_albums = self.spotify.artist_albums(artist_id=artist_id,
                                                           album_type=ALBUM,
                                                           country=settings.SPOTIFY_MARKET,
                                                           limit=limit)
                albums = [item_to_spotify_release(item, ALBUM) for item in result_albums['items']]
                artist_releases.extend(albums)
            except ConnectionError:
                print(("> Could not establish connection while fetching "
                       "albums for artist with id {}. Skipping.").format(artist_id))
            except JSONDecodeError:
                print(("> Could not decode JSON response "
                       "of artist with id {}. Skipping.").format(artist_id))

            # Singles
            try:
                result_singles = self.spotify.artist_albums(artist_id=artist_id,
                                                            album_type=SINGLE,
                                                            country=settings.SPOTIFY_MARKET,
                                                            limit=limit)
                singles = [item_to_spotify_release(item, SINGLE) for item in result_singles['items']]
                artist_releases.extend(singles)
            except ConnectionError:
                print(("> Could not establish connection while fetching "
                       "singles for artist with id {}. Skipping.").format(artist_id))
            except JSONDecodeError:
                print(("> Could not decode JSON response "
                       "of artist with id {}. Skipping.").format(artist_id))

            # Filter
            filtered_releases = self.filter_releases(artist_releases)
            if filtered_releases:
                result[artist_id] = filtered_releases
        return result

    def process(self):
        print("> Start ({}).".format(datetime.now()))
        artist_ids = self.get_ids_of_followed_artists()
        releases_per_artist = self.get_releases_per_artist(artist_ids)
        twitter_status_strings = create_twitter_status_strings_from_releases_per_artist(releases_per_artist)
        if not self.is_first_run:
            print("> {} releases will be tweeted.".format(len(twitter_status_strings)))
            # notify
        else:
            print(("Zero notifications at first run. "
                   "The cache is now initialized and the script will run as promised in the "
                   "next run. All releases until now will not be tweeted anymore."))
        print("> Done ({}).".format(datetime.now()))


if __name__ == '__main__':
    for user_name, user_data in settings.SPOTIFY_USERS.items():
        print("Processing Spotify user", user_name)
        s = SpotifyReleaseGun(user_data)
        s.process()
