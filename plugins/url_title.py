import plugin
from lxml import html
import fetcher
import re


def get_url_title(irc, user, target, line):
    # TODO: better regexp, e.g. parse '#' correctly
    regexp = re.compile(r'''http[s]?://
                            (?:[a-zA-Z]
                             |[0-9]
                             |[$-_@.&+]
                             |[!*\(\),]
                             |(?:%[0-9a-fA-F][0-9a-fA-F])
                            )+''', re.I | re.X)
    urls = re.findall(regexp, line)
    for url in urls:
        page = fetcher.fetch_page(url)
        tree = html.fromstring(page)
        title = tree.xpath('/html/head/title/text()')
        if len(title) >= 1:
            message = title[0].replace('\n',' ')
            message = re.sub( '\s+', ' ', message).strip()
            msg = 'URL title: %s' % message
            msg = msg.encode('ascii', 'replace')
            irc.msg(target, msg)

plugin.add_plugin('https?://', get_url_title)
