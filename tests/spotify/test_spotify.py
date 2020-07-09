from unittest import mock
from unittest import TestCase

from plugins import spotify
from tests.resource import suite_resource, content_of


SPOTIFY_URI = 'spotify:track:2KH16WveTQWT6KOG9Rg6e2'
SPOTIFY_URL = 'https://open.spotify.com/track/2KH16WveTQWT6KOG9Rg6e2'
SPOTIFY_TITLE = 'Eye of the Tiger, a song by Survivor on Spotify'


class TestSpotify(TestCase):

    def setUp(self):
        self.irc = mock.MagicMock()
        self.patch_fetcher = mock.patch('plugins.spotify.fetcher')
        self.mock_fetcher = self.patch_fetcher.start()

    def tearDown(self):
        self.patch_fetcher.stop()

    def test_build_spotify_url(self):
        expected_url = SPOTIFY_URL
        self.assertEqual(
            expected_url,
            spotify.build_spotify_url_from_uri(SPOTIFY_URI))

    def test_spotify_uri_resolve(self):
        self.mock_fetcher.fetch_page.return_value = self._fetch_page_resource('spotify.html')
        expected_title = 'Title: %s - %s' % (SPOTIFY_TITLE, SPOTIFY_URL)
        spotify.resolve_spotify_uri(self.irc, 'user', 'target', 'dummy text %s dummy' % SPOTIFY_URI)

        self.mock_fetcher.fetch_page.assert_called_with(SPOTIFY_URL)
        self.irc.msg.assert_called_with('target', expected_title)

    @staticmethod
    def _fetch_page_resource(page):
        return content_of(suite_resource(__file__, page))
