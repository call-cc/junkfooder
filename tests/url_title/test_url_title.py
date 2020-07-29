from unittest import mock
from unittest import TestCase

from plugins import url_title
from tests.resource import suite_resource, content_of


class TestUrlTitle(TestCase):

    def setUp(self):
        self.irc = mock.MagicMock()
        self.patch_fetcher = mock.patch('plugins.url_title.fetcher')
        self.mock_fetcher = self.patch_fetcher.start()

    def tearDown(self):
        self.patch_fetcher.stop()

    def test_url_encode(self):
        self.mock_fetcher.fetch_page.return_value = self._fetch_page_resource('bbc.html')
        expected_title = 'URL title: BBC - Homepage'
        url_title.get_url_title(self.irc, 'user', 'target', 'https://dummyurl.com')

        self.irc.msg.assert_called_with('target', expected_title)

    def test_url_unicode_encode(self):
        self.mock_fetcher.fetch_page.return_value = self._fetch_page_resource('batar.html')
        expected_title = 'URL title: TTK BATÁR Utazástermelő'
        url_title.get_url_title(self.irc, 'user', 'target', 'https://dummyurl.com')

        self.irc.msg.assert_called_with('target', expected_title)

    def test_url_unicode2_encode(self):
        self.mock_fetcher.fetch_page.return_value = self._fetch_page_resource('index.html')
        expected_title = 'URL title: Alma - Kürtöld - Tóparti'
        url_title.get_url_title(self.irc, 'user', 'target', 'https://dummyurl.com')

        self.irc.msg.assert_called_with('target', expected_title)

    def test_url_youtube_title_in_body(self):
        self.mock_fetcher.fetch_page.return_value = self._fetch_page_resource('youtube_title_in_body.html')
        expected_title = 'URL title: Youtube: why is title under /html/body/title?'
        url_title.get_url_title(self.irc, 'user', 'target', 'https://dummyurl.com')

        self.irc.msg.assert_called_with('target', expected_title)

    @staticmethod
    def _fetch_page_resource(page):
        return content_of(suite_resource(__file__, page))
