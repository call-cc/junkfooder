import plugin
import fetcher
from lxml import html


def a38(irc, user, target, msg):
    url = 'http://www.a38.hu/en/restaurant'
    data = fetcher.get_page(url, 'a38.html')
    tree = html.fromstring(data)
    path = '//div[@class="foodCard__foodlist"]/text()'

    menu = tree.xpath(path)
    if menu == []:
        line = 'No menu found @ A38'
        irc.msg(target, line)
        return

    menu = tree.xpath(path)
    menu = ' | '.join(map(str.strip, menu))

    line = 'Current A38 menu: %s' % menu
    irc.msg(target, line.encode('ascii', 'replace'))

plugin.add_plugin('^!a38\Z', a38)
plugin.add_help('!a38', 'Query A-38 menu')
