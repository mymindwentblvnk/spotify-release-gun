import unittest
from mock import patch
from hamcrest import assert_that, equal_to, is_
from spotify_release_tweeter import SpotifyRelease


class TestSpotifyReleaseTweeter(unittest.TestCase):

    @patch.object(SpotifyRelease, '__init__')
    def test_test(self, release_init):
        release_init.return_value = None
        SpotifyRelease()
        assert_that(4 == 4, is_(True))
