from twython import Twython


class TwitterAdapter:
    """
    A class that connects you to your Twitter account and posts a list of RedditSubmission objects.
    """
    __t = None

    def __init__(self, user):
        appKey = user.APP_KEY
        appSecret = user.APP_SECRET
        oauthToken = user.OAUTH_TOKEN
        oauthTokenSecret = user.OAUTH_TOKEN_SECRET
        self.__t = Twython(appKey, appSecret, oauthToken, oauthTokenSecret)

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
        twitter = self.__t

        try:
            status = item.toTwitterString()
            twitter.update_status(status=status[:140])
        except:
            twitter.update_status(status=item[:140])