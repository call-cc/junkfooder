import plugin
import fetcher
import time
from lxml import html


def a38(irc, user, target, msg):
    url = 'http://www.a38.hu/en/restaurant'
    data = fetcher.get_page(url, 'a38.html')
    tree = html.fromstring(data)
    path = '//div[@class="etterem-content-napiMenu"]/p[2]/strong/text()'
    today = time.strftime("%Y.%m.%d")

    menu = tree.xpath(path)
    if menu == []:
        line = 'No menu for %s @ A38' % today
        irc.msg(target, line)
        return

    menu = tree.xpath(path)
    menu = ''.join(menu)
    menu = menu.replace('\n', ' | ')

    line = 'Menu for %s @ A38: %s' % (today, menu)
    irc.msg(target, line.encode('ascii', 'replace'))

plugin.add_plugin('^!a38\Z', a38)
plugin.add_help('!a38', 'Query A-38 menu')
