import os
from unittest import TestCase

from plugins.youtube import YouTube


class TestYouTube(TestCase):
    def test_query_format(self):
        self.assertURLEncodedQuery({"search_query": "findThis"}, "findThis")
        self.assertURLEncodedQuery({"search_query": "find this"}, "find this")
        self.assertURLEncodedQuery({"search_query": "find?this"}, "find?this")

    def test_youtube_content_parsing(self):
        requests = RequestsMock()
        youtube = YouTube(requests=requests)

        result = youtube.search("foobar")

        self.assertEqual(19, len(result))

        for url, title in result.items():
            self.assertTrue(url.startswith("https://www.youtube.com/watch?v="))

    def assertURLEncodedQuery(self, expected_query, original_query):
        requests = RequestsMock()
        youtube = YouTube(requests=requests)
        youtube.search(original_query)
        self.assertEqual(
            "https://www.youtube.com/results",
            requests.url
        )
        self.assertEqual(expected_query, requests.params)


class RequestsMock(object):
    def __init__(self, resource='foobar.html'):
        self.result = os.path.join(os.path.dirname(__file__), 'resources', resource)
        self.url = ""
        self.params = {}

    def get(self, url, **kwargs):
        self.url = url
        self.params = kwargs.get("params")
        with open(self.result) as f:
            return ResponseMock(f.read())


class ResponseMock(object):
    def __init__(self, content):
        self.content = content
