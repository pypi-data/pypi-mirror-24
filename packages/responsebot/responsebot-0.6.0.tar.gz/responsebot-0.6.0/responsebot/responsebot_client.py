from __future__ import absolute_import

from decorator import decorate
from tweepy.error import TweepError, RateLimitError

from responsebot.common.constants import TWITTER_PAGE_DOES_NOT_EXISTS_ERROR, TWITTER_TWEET_NOT_FOUND_ERROR, \
    TWITTER_USER_NOT_FOUND_ERROR, TWITTER_DELETE_OTHER_USER_TWEET, TWITTER_ACCOUNT_SUSPENDED_ERROR,\
    TWITTER_USER_IS_NOT_LIST_MEMBER_SUBSCRIBER, TWITTER_AUTOMATED_REQUEST_ERROR, TWITTER_OVER_CAPACITY_ERROR,\
    TWITTER_DAILY_STATUS_UPDATE_LIMIT_ERROR, TWITTER_CHARACTER_LIMIT_ERROR_1, TWITTER_CHARACTER_LIMIT_ERROR_2, \
    TWITTER_STATUS_DUPLICATE_ERROR
from responsebot.common.exceptions import APIQuotaError, AutomatedRequestError, OverCapacityError,\
    DailyStatusUpdateError, CharacterLimitError, StatusDuplicateError
from responsebot.models import Tweet, User, List
from responsebot.utils.tweepy import tweepy_list_to_json


def api_error_handle(func):
    def func_wrapper(f, *args, **kwargs):
        try:
            return f(*args, **kwargs)
        except RateLimitError as e:
            raise APIQuotaError(str(e))
        except TweepError as e:
            if e.api_code == TWITTER_AUTOMATED_REQUEST_ERROR:
                raise AutomatedRequestError
            elif e.api_code == TWITTER_OVER_CAPACITY_ERROR:
                raise OverCapacityError
            elif e.api_code in [TWITTER_CHARACTER_LIMIT_ERROR_1, TWITTER_CHARACTER_LIMIT_ERROR_2]:
                raise CharacterLimitError
            elif e.api_code == TWITTER_DAILY_STATUS_UPDATE_LIMIT_ERROR:
                raise DailyStatusUpdateError
            elif e.api_code == TWITTER_STATUS_DUPLICATE_ERROR:
                raise StatusDuplicateError
            else:
                raise

    return decorate(func, func_wrapper)


class ResponseBotClient(object):
    """
    Wrapper for all Twitter API clients.
    """
    def __init__(self, client, config):
        self._client = client
        self._current_user = None
        self.config = config

    @property
    def tweepy_api(self):
        """
        Get the actual client object.

        :return: the actual client object
        """
        return self._client

    def get_current_user(self):
        if self._current_user is None:
            self._current_user = User(self._client.me()._json)
        return self._current_user

    @api_error_handle
    def tweet(self, text, in_reply_to=None, filename=None, file=None):
        """
        Post a new tweet.

        :param text: the text to post
        :param in_reply_to: The ID of the tweet to reply to
        :param filename: If `file` param is not provided, read file from this path
        :param file: A file object, which will be used instead of opening `filename`. `filename` is still required, for
        MIME type detection and to use as a form field in the POST data
        :return: Tweet object
        """

        if filename is None:
            return Tweet(self._client.update_status(status=text, in_reply_to_status_id=in_reply_to)._json)
        else:
            return Tweet(self._client.update_with_media(filename=filename, file=file,
                                                        status=text, in_reply_to_status_id=in_reply_to)._json)

    def retweet(self, id):
        """
        Retweet a tweet.

        :param id: ID of the tweet in question
        :return: True if success, False otherwise
        """
        try:
            self._client.retweet(id=id)
            return True
        except TweepError as e:
            if e.api_code == TWITTER_PAGE_DOES_NOT_EXISTS_ERROR:
                return False
            raise

    def get_tweet(self, id):
        """
        Get an existing tweet.

        :param id: ID of the tweet in question
        :return: Tweet object. None if not found
        """
        try:
            return Tweet(self._client.get_status(id=id)._json)
        except TweepError as e:
            if e.api_code == TWITTER_TWEET_NOT_FOUND_ERROR:
                return None
            raise

    def get_user(self, id):
        """
        Get a user's info.

        :param id: ID of the user in question
        :return: User object. None if not found
        """
        try:
            return User(self._client.get_user(user_id=id)._json)
        except TweepError as e:
            if e.api_code == TWITTER_USER_NOT_FOUND_ERROR:
                return None
            raise

    def remove_tweet(self, id):
        """
        Delete a tweet.

        :param id: ID of the tweet in question
        :return: True if success, False otherwise
        """
        try:
            self._client.destroy_status(id=id)
            return True
        except TweepError as e:
            if e.api_code in [TWITTER_PAGE_DOES_NOT_EXISTS_ERROR, TWITTER_DELETE_OTHER_USER_TWEET]:
                return False
            raise

    def follow(self, user_id, notify=False):
        """
        Follow a user.

        :param user_id: ID of the user in question
        :param notify: whether to notify the user about the following
        :return: user that are followed
        """
        try:
            return User(self._client.create_friendship(user_id=user_id, follow=notify)._json)
        except TweepError as e:
            if e.api_code in [TWITTER_ACCOUNT_SUSPENDED_ERROR]:
                return self.get_user(user_id)
            raise

    def unfollow(self, user_id):
        """
        Follow a user.

        :param user_id: ID of the user in question
        :return: The user that were unfollowed
        """
        return User(self._client.destroy_friendship(user_id=user_id)._json)

    ###################################################################################
    # Lists
    ###################################################################################
    @api_error_handle
    def create_list(self, name, mode='public', description=None):
        """
        Create a list

        :param name: Name of the new list
        :param mode: :code:`'public'` (default) or :code:`'private'`
        :param description: Description of the new list
        :return: The new list object
        :rtype: :class:`~responsebot.models.List`
        """
        return List(tweepy_list_to_json(self._client.create_list(name=name, mode=mode, description=description)))

    @api_error_handle
    def destroy_list(self, list_id):
        """
        Destroy a list

        :param list_id: list ID number
        :return: The destroyed list object
        :rtype: :class:`~responsebot.models.List`
        """
        return List(tweepy_list_to_json(self._client.destroy_list(list_id=list_id)))

    @api_error_handle
    def update_list(self, list_id, name=None, mode=None, description=None):
        """
        Update a list

        :param list_id: list ID number
        :param name: New name for the list
        :param mode: :code:`'public'` (default) or :code:`'private'`
        :param description: New description of the list
        :return: The updated list object
        :rtype: :class:`~responsebot.models.List`
        """
        return List(tweepy_list_to_json(
            self._client.update_list(list_id=list_id, name=name, mode=mode, description=description))
        )

    @api_error_handle
    def lists(self):
        """
        List user's lists

        :return: list of :class:`~responsebot.models.List` objects
        """
        return [List(tweepy_list_to_json(list)) for list in self._client.lists_all()]

    @api_error_handle
    def lists_memberships(self):
        """
        List lists which user was added

        :return: list of :class:`~responsebot.models.List` objects
        """
        return [List(tweepy_list_to_json(list)) for list in self._client.lists_memberships()]

    @api_error_handle
    def lists_subscriptions(self):
        """
        List lists which user followed

        :return: list of :class:`~responsebot.models.List` objects
        """
        return [List(tweepy_list_to_json(list)) for list in self._client.lists_subscriptions()]

    @api_error_handle
    def list_timeline(self, list_id, since_id=None, max_id=None, count=20):
        """
        List the tweets of specified list.

        :param list_id: list ID number
        :param since_id: results will have ID greater than specified ID (more recent than)
        :param max_id: results will have ID less than specified ID (older than)
        :param count: number of results per page
        :return: list of :class:`~responsebot.models.Tweet` objects
        """
        statuses = self._client.list_timeline(list_id=list_id, since_id=since_id, max_id=max_id, count=count)
        return [Tweet(tweet._json) for tweet in statuses]

    @api_error_handle
    def get_list(self, list_id):
        """
        Get info of specified list

        :param list_id: list ID number
        :return: :class:`~responsebot.models.List` object
        """
        return List(tweepy_list_to_json(self._client.get_list(list_id=list_id)))

    @api_error_handle
    def add_list_member(self, list_id, user_id):
        """
        Add a user to list

        :param list_id: list ID number
        :param user_id: user ID number
        :return: :class:`~responsebot.models.List` object
        """
        return List(tweepy_list_to_json(self._client.add_list_member(list_id=list_id, user_id=user_id)))

    @api_error_handle
    def remove_list_member(self, list_id, user_id):
        """
        Remove a user from a list

        :param list_id: list ID number
        :param user_id: user ID number
        :return: :class:`~responsebot.models.List` object
        """
        return List(tweepy_list_to_json(self._client.remove_list_member(list_id=list_id, user_id=user_id)))

    @api_error_handle
    def list_members(self, list_id):
        """
        List users in a list

        :param list_id: list ID number
        :return: list of :class:`~responsebot.models.User` objects
        """
        return [User(user._json) for user in self._client.list_members(list_id=list_id)]

    @api_error_handle
    def is_list_member(self, list_id, user_id):
        """
        Check if a user is member of a list

        :param list_id: list ID number
        :param user_id: user ID number
        :return: :code:`True` if user is member of list, :code:`False` otherwise
        """
        try:
            return bool(self._client.show_list_member(list_id=list_id, user_id=user_id))
        except TweepError as e:
            if e.api_code == TWITTER_USER_IS_NOT_LIST_MEMBER_SUBSCRIBER:
                return False
            raise

    @api_error_handle
    def subscribe_list(self, list_id):
        """
        Subscribe to a list

        :param list_id: list ID number
        :return: :class:`~responsebot.models.List` object
        """
        return List(tweepy_list_to_json(self._client.subscribe_list(list_id=list_id)))

    @api_error_handle
    def unsubscribe_list(self, list_id):
        """
        Unsubscribe to a list

        :param list_id: list ID number
        :return: :class:`~responsebot.models.List` object
        """
        return List(tweepy_list_to_json(self._client.unsubscribe_list(list_id=list_id)))

    @api_error_handle
    def list_subscribers(self, list_id):
        """
        List subscribers of a list

        :param list_id: list ID number
        :return: :class:`~responsebot.models.User` object
        """
        return [User(user._json) for user in self._client.list_subscribers(list_id=list_id)]

    @api_error_handle
    def is_subscribed_list(self, list_id, user_id):
        """
        Check if user is a subscribed of specified list

        :param list_id: list ID number
        :param user_id: user ID number
        :return: :code:`True` if user is subscribed of list, :code:`False` otherwise
        """
        try:
            return bool(self._client.show_list_subscriber(list_id=list_id, user_id=user_id))
        except TweepError as e:
            if e.api_code == TWITTER_USER_IS_NOT_LIST_MEMBER_SUBSCRIBER:
                return False
            raise
