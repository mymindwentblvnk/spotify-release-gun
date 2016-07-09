from twython import Twython
from config import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

class TwitterAdapter:
    """
    A class that connects you to your Twitter account and posts a list of RedditSubmission objects.
    """
    __t = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def tweetList(self, items):
        """
        Iterates over a list of RedditSubmission objects and posts them to your Twitter timeline.
        :param submissions: List of RedditSubmission objects.
        """
        for item in items:
            self.tweet(item)

    def tweet(self, item):
        """
        Tweets on your timeline
        :param item: Has to have a toTwitterString method
        """
        status = item.toTwitterString()
        twitter = self.__t
        twitter.update_status(status=status[:140])