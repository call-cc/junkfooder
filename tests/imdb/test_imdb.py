from unittest import mock
from unittest import TestCase

from plugins import imdb
from tests.resource import suite_resource, content_of


class TestIMDB(TestCase):

    def setUp(self):
        self.irc = mock.MagicMock()
        self.patch_fetcher = mock.patch('plugins.imdb.fetcher')
        self.mock_fetcher = self.patch_fetcher.start()

    def tearDown(self):
        self.patch_fetcher.stop()

    def test_imdb(self):
        self.mock_fetcher.fetch_page.return_value = self._fetch_page_resource('sample.html')
        expected_answer = 'https://www.imdb.com/title/tt2395427/ -- Avengers: Age of Ultron (2015) - IMDb'
        imdb.search_imdb(self.irc, 'user', 'target', 'ultron')
        self.irc.msg.assert_called_with('target', expected_answer)

    def test_imdb_empty_result(self):
        self.mock_fetcher.fetch_page.return_value = 'empty'
        expected_answer = 'That is the story of your life...'
        imdb.search_imdb(self.irc, 'user', 'target', 'empty')
        self.irc.msg.assert_called_with('target', expected_answer)

    @staticmethod
    def _fetch_page_resource(page):
        return content_of(suite_resource(__file__, page))
