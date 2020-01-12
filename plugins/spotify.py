import re
from lxml import html

import fetcher
import plugin


URL = r'https://open.spotify.com/%s/%s'


def build_spotify_url_from_uri(uri):
    uri_parts = uri.split(':')
    unit = uri_parts[1]
    spotify_id = uri_parts[2]
    return URL % (unit, spotify_id)


def resolve_spotify_uri(irc, user, target, line):
    regexp = re.compile(
        r'spotify:[a-z]*:[a-zA-Z0-9]*', re.IGNORECASE)
    uris = re.findall(regexp, line)
    for uri in uris:
        url = build_spotify_url_from_uri(uri)
        page = fetcher.fetch_page(url)
        tree = html.fromstring(page)
        title = tree.xpath('/html/head/title/text()')
        if len(title) >= 1:
            msg = 'Title: %s - %s' % (title[0], url)
            msg = msg.replace('\n', ' ')
            msg = re.sub(r'\s+', ' ', msg).strip()
            irc.msg(target, msg)


plugin.add_plugin('spotify:', resolve_spotify_uri)
