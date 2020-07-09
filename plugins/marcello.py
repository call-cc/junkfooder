import plugin
import fetcher
from lxml import html


def marcello(irc, user, target, msg):
    url = 'https://www.marcelloetterem.hu'
    data = fetcher.get_page(url, 'marcello.tmp')
    tree = html.fromstring(data)
    menu = []
    # The menu in 3 paragraph
    for i in range(1, 4):
        path = '//div[@class="newsflash"]/p[{}]/strong/text()'.format(i)
        menu = menu + tree.xpath(path)
    # Menu pricing info
    for i in range(1, 5):
        path = '//div[@class="newsflash"]/h6[{}]/text()'.format(i)
        menu = menu + tree.xpath(path)

    if menu == []:
        line = 'No menu found @ Marcello'
        irc.msg(target, line)
        return

    menu = ' | '.join(menu)

    line = 'Current Marcello menu: %s' % menu
    irc.msg(target, line.title().encode('ascii', 'replace'))


plugin.add_plugin('^!marcello\Z', marcello)
plugin.add_help('!marcello', 'Query Marcello menu')
