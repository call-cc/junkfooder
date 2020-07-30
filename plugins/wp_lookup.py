import wikipedia

import plugin


def wikipedia_lookup(irc, _user, target, msg):
    _cmd, title = msg.split(None, 1)
    wikipedia.set_lang('en')

    try:
        page = wikipedia.summary(title, sentences=1)
        page += " For more: " + wikipedia.page(title).url
    except wikipedia.DisambiguationError as exc:
        pages = ' | '.join(exc.options[:10])
        results = '"%s" may refer to: %s' % (title, pages)
        irc.msg(target, results)
        return
    except wikipedia.PageError:
        line = 'No such page: %s' % title
        irc.msg(target, line)
        return

    irc.msg(target, page)


plugin.add_plugin('^!wp ', wikipedia_lookup)
plugin.add_help('!wp', 'Query Wikipedia. Example: !wp ozric tentacles')
