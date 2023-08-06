import logging

from responsebot.common.constants import TWITTER_NON_TWEET_EVENTS
from responsebot.models import TweetFilter


class ResponseBotListener(object):
    """
    Forward received tweets from :class:`~responsebot.responsebot_stream.ResponseBotStream`
    """
    def __init__(self, handler_classes, client):
        """
        Inits the listener and tries to create handler instances from discovered user's handler classes

        :param handler_classes: List of :class:`~responsebot.handlers.base.BaseTweetHandler`'s derived classes
        :param client: Some Twitter API client for authentication. E.g. :class:`~responsebot.tweet_client.TweetClient`
        """
        self.client = client
        self.handlers = []

        self.register_handlers(handler_classes)

    def register_handlers(self, handler_classes):
        """
        Create handlers from discovered handler classes

        :param handler_classes: List of :class:`~responsebot.handlers.base.BaseTweetHandler`'s derived classes
        """
        for handler_class in handler_classes:
            self.handlers.append(handler_class(client=self.client))
            logging.info('Successfully registered {handler_class}'.format(
                handler_class=getattr(handler_class, '__name__', str(handler_class)))
            )

    def on_tweet(self, tweet):
        """
        Callback to receive tweet from :class:`~responsebot.responsebot_stream.ResponseBotStream`. Tries to forward the
        received tweet to registered handlers.

        :param tweet: An object containing a tweet's text and metadata
        :type tweet: :class:`~responsebot.models.Tweet`
        """
        logging.info(u'Received tweet: `{message}`'.format(message=tweet.text))

        for handler in self.handlers:
            if not handler.catch_self_tweets and self.is_self_tweet(tweet):
                continue

            if not handler.filter.match_tweet(tweet=tweet, user_stream=self.client.config.get('user_stream')):
                continue

            handler.on_tweet(tweet)

    def on_event(self, event):
        """
        Callback to receive events from :class:`~responsebot.responsebot_stream.ResponseBotStream`. Tries to forward the
        received event to registered handlers.

        :param event: The received event
        :type event: :class:`~responsebot.models.Event`
        error from a custom handler
        """
        if event.event not in TWITTER_NON_TWEET_EVENTS:
            logging.warning(u'Received unknown twitter event {event}'.format(event=event.event))
            return

        logging.info(u'Received event {event}'.format(event=event.event))

        for handler in self.handlers:
            handler.on_event(event)

    def is_self_tweet(self, tweet):
        return self.client.get_current_user().id == tweet.user.id

    def get_merged_filter(self):
        """
        Return merged filter from list of handlers

        :return: merged filter
        :rtype: :class:`~responsebot.models.TweetFilter`
        """
        track = set()
        follow = set()

        for handler in self.handlers:
            track.update(handler.filter.track)
            follow.update(handler.filter.follow)

        return TweetFilter(track=list(track), follow=list(follow))
