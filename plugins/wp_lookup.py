import wikipedia

import plugin


def wp(irc, user, target, msg):
    cmd, title = msg.split(None, 1)
    wikipedia.set_lang('en')

    try:
        page = wikipedia.summary(title, sentences=1)
        page += " For more: " + wikipedia.page(title).url
    except wikipedia.DisambiguationError as e:
        pages = ' | '.join([s
                            for s in e.options[:10]])
        results = '"%s" may refer to: %s' % (title, pages)
        irc.msg(target, results)
        return
    except wikipedia.PageError:
        line = 'No such page: %s' % title
        irc.msg(target, line)
        return

    page = page
    irc.msg(target, page)


plugin.add_plugin('^!wp ', wp)
plugin.add_help('!wp', 'Query Wikipedia. Example: !wp ozric tentacles')
