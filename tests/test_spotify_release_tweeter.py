import unittest
from mock import patch
from mock import PropertyMock
from hamcrest import assert_that, equal_to, is_

from twython import Twython
import pickle
import spotify_release_tweeter
import spotipy.util

from spotify_release_tweeter import SpotifyReleaseTweeter
from spotify_release_tweeter import create_twitter_status_strings_from_releases_per_artist
from spotify_release_tweeter import Tweeter


class TestSpotifyReleaseTweeter(unittest.TestCase):
    @patch.object(SpotifyReleaseTweeter, 'process')
    @patch.object(Tweeter, 'tweet_list')
    @patch.object(Twython, '__init__')
    @patch.object(pickle, 'load')
    @patch.object(pickle, 'dump')
    @patch.object(spotify_release_tweeter, 'is_first_run')
    @patch.object(spotify_release_tweeter.AlreadyHandledCache, 'update')
    @patch.object(spotipy.util, 'prompt_for_user_token')
    @patch.object(spotipy.Spotify, '__init__')
    @patch.object(spotipy.Spotify, 'current_user_followed_artists')
    @patch.object(spotipy.Spotify, 'artist_albums')
    def test_test(self,
                  spotipy_artist_albums,
                  spotipy_current_user_followed_artists,
                  spotipy_init,
                  spotipy_util_prompt_for_user_token,
                  cache_update,
                  is_first_run,
                  pickle_dump,
                  pickle_load,
                  twython_init,
                  twython_tweet_list,
                  process):
        spotipy_artist_albums.side_effect = [
            # ID1
            {
                'items': [{
                    'id': 'R_ID_11',
                    'name': 'R_Name_11',
                    'album_type': 'A_Type_11',
                    'artists': [{'name': 'A_Name_11'},
                                {'name': 'Not_Read_Artist_Name'}, ]
                }]
            },
            {
                'items': [{
                    'id': 'R_ID_12',
                    'name': 'R_Name_12',
                    'album_type': 'A_Type_12',
                    'artists': [{'name': 'A_Name_12'},
                                {'name': 'Not_Read_Artist_Name'}, ]
                }]
            },
            # ID2
            {
                'items': [{
                    'id': 'R_ID_21',
                    'name': 'R_Name_21',
                    'album_type': 'A_Type_21',
                    'artists': [{'name': 'A_Name_21'},
                                {'name': 'Not_Read_Artist_Name'}, ]
                }]

            },
            {
                'items': [{
                    'id': 'R_ID_22',
                    'name': 'R_Name_22',
                    'album_type': 'A_Type_22',
                    'artists': [{'name': 'A_Name_22'},
                                {'name': 'Not_Read_Artist_Name'}, ]
                }]

            },
            # ID3
            {
                'items': [{
                    'id': 'R_ID_31',
                    'name': 'R_Name_31',
                    'album_type': 'A_Type_31',
                    'artists': [{'name': 'A_Name_31'},
                                {'name': 'Not_Read_Artist_Name'}, ]
                }]

            },
            {
                'items': [{
                    'id': 'R_ID_32',
                    'name': 'R_Name_32',
                    'album_type': 'A_Type_32',
                    'artists': [{'name': 'A_Name_32'},
                                {'name': 'Not_Read_Artist_Name'}, ]
                }]

            },
        ]
        spotipy_current_user_followed_artists.side_effect = [
            {
                'artists': {
                    'items': [{'id': 'ID1'}, {'id': 'ID2'}, {'id': 'ID3'}]
                },

            },
            {'artists': {'items': []}}
        ]
        spotipy_init.return_value = None
        spotipy_util_prompt_for_user_token.return_value = None
        cache_update.return_value = None
        is_first_run.return_value = None
        pickle_dump.return_value = None
        pickle_load.return_value = ['R_ID_32', 'R_ID_21', 'Not_Relevant_Cached_ID', 'R_ID_11', ]
        twython_init.return_value = None
        twython_tweet_list.return_value = None
        process.return_value = None

        tweeter = SpotifyReleaseTweeter()

        artist_ids = tweeter.get_ids_of_followed_artists()
        assert_that(artist_ids, equal_to(['ID1', 'ID2', 'ID3']))

        releases_per_artist = tweeter.get_releases_per_artist(artist_ids)


        twitter_status_strings = create_twitter_status_strings_from_releases_per_artist(releases_per_artist)
