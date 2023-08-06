from unittest.case import TestCase

from tweepy.error import TweepError

from responsebot.responsebot_stream import ResponseBotStream

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock


class TweetStreamTestCase(TestCase):
    def test_terminate_on_critical_error(self):
        exception = TweepError(reason='Stream object already connected!')
        with patch('responsebot.responsebot_stream.tweepy.Stream.filter', side_effect=exception) as mock_stream:
            mock_client = MagicMock(config=MagicMock(get=MagicMock(return_value=False)))
            stream = ResponseBotStream(client=mock_client, listener=MagicMock())

            self.assertRaises(TweepError, stream.start)
            self.assertEqual(mock_stream.call_count, 1)

    def test_filter_using_merged_filter(self):
        merged_filter = MagicMock(track=['track'], follow=['follow'])
        mock_client = MagicMock(config=MagicMock(get=MagicMock(return_value=False)))
        stream = ResponseBotStream(client=mock_client, listener=MagicMock(
                get_merged_filter=MagicMock(return_value=merged_filter)))

        with patch('responsebot.responsebot_stream.tweepy.Stream.filter') as mock_filter_call:
            stream.start(retry_limit=0)

            mock_filter_call.assert_called_once_with(track=merged_filter.track, follow=merged_filter.follow)

    @patch('responsebot.responsebot_stream.tweepy.Stream.filter',
           side_effect=AttributeError('\'NoneType\' object has no attribute \'strip\''))
    def test_ignore_tweepy_attribute_error(self, mock_stream):
        mock_client = MagicMock(config=MagicMock(get=MagicMock(return_value=False)))
        stream = ResponseBotStream(client=mock_client, listener=MagicMock())
        stream.start(retry_limit=1)

        self.assertEqual(mock_stream.call_count, 2)

    @patch('responsebot.responsebot_stream.tweepy.Stream.filter',
           side_effect=AttributeError('Some error that is not NoneType'))
    def test_raise_attribute_error(self, mock_stream):
        mock_client = MagicMock(config=MagicMock(get=MagicMock(return_value=False)))
        stream = ResponseBotStream(client=mock_client, listener=MagicMock())
        self.assertRaises(AttributeError, stream.start)

    def test_use_user_stream(self):
        mock_client = MagicMock(config=MagicMock(get=MagicMock(return_value=True)))
        merged_filter = MagicMock(track=['track'])
        stream = ResponseBotStream(client=mock_client, listener=MagicMock(
                get_merged_filter=MagicMock(return_value=merged_filter)))

        with patch('responsebot.responsebot_stream.tweepy.Stream.userstream') as mock_user_stream_call:
            stream.start(retry_limit=0)

            mock_user_stream_call.assert_called_once_with(track=merged_filter.track)
