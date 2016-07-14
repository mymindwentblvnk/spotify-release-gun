from twython import Twython
from util import log


class TwitterAdapter:
    """
    A class that connects you to your Twitter account and posts a list of items
    with a to_twitter_string method.
    """
    __t = None

    def __init__(self, user):
        appKey = user.APP_KEY
        appSecret = user.APP_SECRET
        oauthToken = user.OAUTH_TOKEN
        oauthTokenSecret = user.OAUTH_TOKEN_SECRET
        self.__t = Twython(appKey, appSecret, oauthToken, oauthTokenSecret)

    def tweet_list(self, items):
        """
        Iterates over a list of items  and posts them to your Twitter timeline.
        :param submissions: List of items objects.
        """
        for item in items:
            self.tweet(item)

    def tweet(self, item):
        """
        Tweets on your timeline
        :param item: Has to have a toTwitterString method
        """
        twitter = self.__t

        status = item.to_twitter_string()
        try:
            twitter.update_status(status=status[:140])
        except:
            # LOGGING
            log("\"%s\" could not be tweeted." % (status))
