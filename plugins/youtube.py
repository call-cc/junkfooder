import random

import requests
from lxml import html

import plugin


def youtube(irc, _user, target, msg):
    videos = YouTube().search(msg)
    title, url = _random_from_dict(videos)
    irc.msg(target, url + " - " + title)


def _random_from_dict(videos):
    index = random.randint(0, len(videos) - 1)
    url = list(videos.keys())[index]
    title = videos[url]
    return title, url


class YouTube(object):
    def __init__(self, **kwargs):
        self.requests = kwargs.get("requests", requests)
        self.base_url = "https://invidious.snopyta.org"

    def search(self, query):
        """
        :type query: str
        :rtype: dict[str, str]
        """
        response = self.requests.get(
            self.base_url + "/search",
            params=dict(
                q=query
            ),
        )
        return self._parse_video_links_from_string(response.content)

    def _parse_video_links_from_string(self, response):
        xpath_query = '//div[@class="h-box"]/p/a[starts-with(@href, "/watch?v=")]'

        tree = html.fromstring(response)
        elements = tree.xpath(xpath_query)

        return self._process_links_from_elements(elements)

    def _process_links_from_elements(self, elements):
        """
        :type elements: list[Element]
        :rtype: dict[str, str]
        """
        links = {}

        for link in elements:
            url = "https://www.youtube.com" + link.get('href')
            links[url] = link.text

        return links


plugin.add_plugin('^!yt', youtube)
plugin.add_help('!yt', 'Search for a youtube video and select a *random* from the search result.')
