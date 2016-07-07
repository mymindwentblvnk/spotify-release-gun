from twython import Twython
from config import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

class TwitterAdapter:
    """
    A class that connects you to your Twitter account and posts a list of RedditSubmission objects.
    """
    __t = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def postStatusList(self, submissions):
        """
        Iterates over a list of RedditSubmission objects and posts them to your Twitter timeline.
        :param submissions: List of RedditSubmission objects.
        """

        for submission in submissions:
            status = submission.get140Characters()
            self.__t.update_status(status=status)