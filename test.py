import unittest
from mock import patch, PropertyMock
from hamcrest import assert_that, equal_to, is_

from twython import Twython
import spotify_release_tweeter
import spotipy.util

from spotify_release_tweeter import SpotifyReleaseTweeter
from spotify_release_tweeter import SpotifyRelease
from spotify_release_tweeter import create_twitter_status_strings_from_releases_per_artist
from spotify_release_tweeter import Tweeter


class TestSpotifyReleaseTweeter(unittest.TestCase):
    @patch.object(SpotifyReleaseTweeter, 'process')
    @patch.object(Tweeter, 'tweet_list')
    @patch.object(Twython, '__init__')
    @patch('spotify_release_tweeter.AlreadyHandledCache.cache', new_callable=PropertyMock, create=True)
    @patch.object(spotify_release_tweeter, 'is_first_run')
    @patch.object(spotify_release_tweeter.AlreadyHandledCache, '__init__')
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
                  cache_init,
                  is_first_run,
                  self_cache,
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
        cache_init.return_value = None
        is_first_run.return_value = False
        self_cache.return_value = ['R_ID_32', 'R_ID_21', 'Not_Relevant_Cached_ID', 'R_ID_11', ]
        twython_init.return_value = None
        twython_tweet_list.return_value = None
        process.return_value = None

        tweeter = SpotifyReleaseTweeter()
        artist_ids = tweeter.get_ids_of_followed_artists()
        assert_that(artist_ids, equal_to(['ID1', 'ID2', 'ID3']))

        releases_per_artist = tweeter.get_releases_per_artist(artist_ids)
        assert_that(len(releases_per_artist), is_(3))
        assert_that(len(releases_per_artist['ID1']), is_(1))
        assert_that(releases_per_artist['ID1'][0].release_id, is_('R_ID_12'))
        assert_that(releases_per_artist['ID1'][0].title, is_('R_Name_12'))
        assert_that(releases_per_artist['ID1'][0].artist_name, is_('A_Name_12'))
        assert_that(releases_per_artist['ID1'][0].url, is_("https://play.spotify.com/album/R_ID_12"))
        assert_that(len(releases_per_artist['ID2']), is_(1))
        assert_that(releases_per_artist['ID2'][0].release_id, is_('R_ID_22'))
        assert_that(releases_per_artist['ID2'][0].title, is_('R_Name_22'))
        assert_that(releases_per_artist['ID2'][0].artist_name, is_('A_Name_22'))
        assert_that(releases_per_artist['ID2'][0].url, is_("https://play.spotify.com/album/R_ID_22"))
        assert_that(len(releases_per_artist['ID3']), is_(1))
        assert_that(releases_per_artist['ID3'][0].release_id, is_('R_ID_31'))
        assert_that(releases_per_artist['ID3'][0].title, is_('R_Name_31'))
        assert_that(releases_per_artist['ID3'][0].artist_name, is_('A_Name_31'))
        assert_that(releases_per_artist['ID3'][0].url, is_("https://play.spotify.com/album/R_ID_31"))

        twitter_status_strings = create_twitter_status_strings_from_releases_per_artist(releases_per_artist)
        assert_that(len(twitter_status_strings), is_(3))
        expected_twitter_status_strings = [
            "A_Name_12 - R_Name_12 (Single) https://play.spotify.com/album/R_ID_12",
            "A_Name_22 - R_Name_22 (Single) https://play.spotify.com/album/R_ID_22",
            "A_Name_31 - R_Name_31 (Album) https://play.spotify.com/album/R_ID_31",
        ]
        assert_that(set(twitter_status_strings), equal_to(set(expected_twitter_status_strings)))

    def test_to_twitter_string_too_long(self):
        test_id = '7D7gToSUwjOPdnpNdQHCKd'
        artist_with_20_characters = [{'name': "12345678901234567890"}]
        title_with_120_characters = "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
        r = SpotifyRelease(release_id=test_id, artists=artist_with_20_characters, title=title_with_120_characters, release_type='Album')
        assert_that(r.to_twitter_string(), equal_to("12345678901234567890 - 1234567890123456789012345678901234567890123456789012345 (Album) https://play.spotify.com/album/7D7gToSUwjOPdnpNdQHCKd"))

    def test_to_twitter_string(self):
        test_id = 'The_ID'
        artist_with_20_characters = [{'name': "The Name"}]
        title_with_120_characters = "The Album Title"
        r = SpotifyRelease(release_id=test_id, artists=artist_with_20_characters, title=title_with_120_characters, release_type='Single')
        assert_that(r.to_twitter_string(), equal_to("The Name - The Album Title (Single) https://play.spotify.com/album/The_ID"))
