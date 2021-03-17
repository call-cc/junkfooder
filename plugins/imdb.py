from lxml import html

import fetcher
import plugin

BASE_URL = 'https://html.duckduckgo.com/html/?q=site:imdb.com '
ERROR_FUN = 'That is the story of your life, isn\'t it?'


def search_imdb(irc, _user, target, line):
    url = BASE_URL + line.replace('!imdb ', '')
    page = fetcher.fetch_page(url)

    if page is None:
        answer = ERROR_FUN
    else:
        try:
            xpath_query = '//a[@class="result__a"]'
            tree = html.fromstring(page)
            elements = tree.xpath(xpath_query)
            answer = elements[0].get('href', ERROR_FUN)
            answer += ' -- ' + elements[0].text_content()
        except (IndexError, TypeError):
            answer = ERROR_FUN

    irc.msg(target, answer)


plugin.add_plugin('^!imdb', search_imdb)
plugin.add_help('!imdb', 'Search for movie or series or actor/actress etc. in imdb.')
