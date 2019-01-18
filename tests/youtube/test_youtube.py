import os
from unittest import TestCase

from plugins.youtube import YouTube


class TestYouTube(TestCase):
    def test_query_format(self):
        self.assertURLEncodedQuery("findThis", "findThis")
        self.assertURLEncodedQuery("find+this", "find this")
        self.assertURLEncodedQuery("find%3Fthis", "find?this")

    def test_youtube_content_parsing(self):
        urllib = URLLibMock()
        youtube = YouTube(urllib=urllib)

        result = youtube.search("foobar")

        self.assertEqual(19, len(result))
        for url, title in result.items():
            self.assertTrue(url.startswith("https://www.youtube.com/watch?v="))

    def assertURLEncodedQuery(self, expected_query, original_query):
        urllib = URLLibMock()
        youtube = YouTube(urllib=urllib)
        youtube.search(original_query)
        self.assertEqual(
            "https://www.youtube.com/results?search_query=" + expected_query,
            urllib.url
        )


class URLLibMock(object):
    def __init__(self, resource='foobar.html'):
        self.result = os.path.join(os.path.dirname(__file__), 'resources', resource)
        self.url = ""

    def urlopen(self, url):
        self.url = url
        with open(self.result) as f:
            return ResponseMock(f.read())


class ResponseMock(object):
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content
