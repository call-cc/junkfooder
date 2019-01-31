from unittest import TestCase

from plugins.youtube import YouTube
from tests.resource import suite_resource, content_of
from tests.request_mock import RequestsMock


class TestYouTube(TestCase):
    def test_query_format(self):
        self.assertURLEncodedQuery({"search_query": "findThis"}, "findThis")
        self.assertURLEncodedQuery({"search_query": "find this"}, "find this")
        self.assertURLEncodedQuery({"search_query": "find?this"}, "find?this")

    def test_youtube_content_parsing(self):
        requests = self._minimal_request_mock()
        youtube = YouTube(requests=requests)

        result = youtube.search("foobar")

        self.assertEqual(19, len(result))

        for url, title in result.items():
            self.assertTrue(url.startswith("https://www.youtube.com/watch?v="))

    def assertURLEncodedQuery(self, expected_query, original_query):
        requests = self._minimal_request_mock()
        youtube = YouTube(requests=requests)
        youtube.search(original_query)
        self.assertEqual(
            "https://www.youtube.com/results",
            requests.url
        )
        self.assertEqual(expected_query, requests.params)

    def _minimal_request_mock(self):
        return RequestsMock(
            content_of(
                suite_resource(__file__, "foobar.html")
            )
        )
