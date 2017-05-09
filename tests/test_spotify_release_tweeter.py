import unittest
from mock import test
from hamcrest import assert_that, equal_to, is_


class TestSpotifyReleaseTweeter(unittest.Testcase):

    def test_test(self):
        assert_that(4 == 4, is_(True))
