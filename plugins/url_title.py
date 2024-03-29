import re

from lxml import html

import fetcher
import plugin


def get_url_title(irc, _user, target, line):
    regexp = re.compile(
        r'https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?\S+)', re.IGNORECASE)
    urls = re.findall(regexp, line)
    for url in urls:
        page = fetcher.fetch_page(url)
        tree = html.fromstring(page)
        title = tree.xpath('/html//title/text()')
        if len(title) >= 1:
            msg = 'URL title: %s' % title[0]
            msg = msg.replace('\n', ' ')
            msg = re.sub(r'\s+', ' ', msg).strip()
            irc.msg(target, msg)


plugin.add_plugin('https?://', get_url_title)
