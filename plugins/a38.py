import requests
from lxml import html

import plugin


def a38(irc, _user, target, msg):
    _a38 = A38(_parse_language(msg))
    irc.msg(target, _a38.fetch_todays_menu())


def _parse_language(msg):
    argv = msg.split()
    if len(argv) < 2:
        return "en"

    return argv[1]


class A38(object):
    LANGUAGES = {
        "hu": "https://www.a38.hu/hu/etterem",
        "en": "https://www.a38.hu/en/restaurant"
    }

    def __init__(self, lang="en", **kwargs):
        self.requests = kwargs.get('requests', requests)
        self.url = A38.LANGUAGES.get(lang, A38.LANGUAGES["en"])

    def fetch_todays_menu(self):
        """
        :rtype: str
        """
        response = self.requests.get(self.url)
        tree = html.fromstring(response.content)

        menu = tree.xpath('//div[@class="foodCard__foodlist"]/text()')  # type: list[str]

        if not menu:
            return 'No menu found @ A38'

        return 'Current A38 menu: %s' % self.format_menu(menu)

    def format_menu(self, menu):
        return ' | '.join(
            [dish.strip() for dish in menu if dish.strip() != ""]
        )


plugin.add_plugin('^!a38', a38)
plugin.add_help('!a38', 'Query A-38 menu. For other languages, please add [en|hu]')
