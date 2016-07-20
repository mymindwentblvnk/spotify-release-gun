from twython import Twython
from the_logger import log

class Twitter:
    """
    A class that connects you to your Twitter account and posts a list of items
    with a to_twitter_string method.
    """
    __t = None

    def __init__(self, user):
        app_key = user.APP_KEY
        app_secret = user.APP_SECRET
        oauth_token = user.OAUTH_TOKEN
        oauth_token_secret = user.OAUTH_TOKEN_SECRET
        self.__t = Twython(
                app_key, app_secret, oauth_token, oauth_token_secret)

    def tweet_list(self, status_list):
        """
        Iterates over a list of status strings and posts them to your Twitter
        timeline.
        :param status_list: List of status strings.
        """
        for status in status_list:
            self.tweet(status)

        # LOGGING
        log("%s Tweet(s) sent." % (len(status_list)))

    def tweet(self, status):
        """
        Tweets a status on your timeline
        :param status: String to tweet.
        """
        twitter = self.__t

        try:
            twitter.update_status(status=status[:140])
        except:
            # LOGGING
            log("Could not be tweeted: %s" % (status))
