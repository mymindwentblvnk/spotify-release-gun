from spotify_module import *
from config import *
from twitter_module import Twitter
from file_operations import save_last_update
from file_operations import load_spotify_cache
from file_operations import save_spotify_cache
from the_logger import log

class SpotifyNotificationTweeter:
    """
    Loads all new releases for a Spotify user and tweets them. Takes also care
    of double tweeting. Just call tweet_new_tweet_new_releases method.
    """

    __spotify_cache = None

    def __init__(self):
        # Load Spotify cache
        self.__spotify_cache = load_spotify_cache()

    def tweet_new_releases(self):
        # Load cache
        __cache = self.__spotify_cache

        def already_tweeted_filter(spotifyRelease):
            """
            Filter method to check if tweet is already in cache
            :param spotifyRelease: Spotify release to check for
            :return: Boolean if release is not already in cache
            """
            return spotifyRelease.id not in __cache


        # Get all new releases for a Spotify user
        user = SpotifyUser()
        s = Spotify(user)
        result = s.get_all_new_releases()

        # Filter all new releases by already tweeted releases
        filtered_result =  list(filter(already_tweeted_filter, result))
        # LOG
        log("%s new releases found." % (len(filtered_result)))

        # Update Spotify cache
        for release in filtered_result:
            self.__spotify_cache.append(release.id)

        # Create tweets from filtered releases
        tweets = self.__create_tweets(filtered_result)

        # Tweet new releases
        user = TwitterUser()
        twitter = Twitter(user)
        twitter.tweet_list(tweets)

        # Save date
        save_last_update()

        # Save Spotify cache
        save_spotify_cache(self.__spotify_cache)


    def __create_tweets(self, twitter_items):
        """
        Creates tweets from a list of items.
        :param twitter_items: items that do provide a to_twitter_string method.
        :return: List of Twitter status strings.
        """
        result = []

        for item in twitter_items:
            try:
                status = item.to_twitter_string()
            except:
                raise Exception("Could not create status from item, "
                    "due to missing to_twitter_string method.")

            result.append(status)

        return result
