import plugin
import wikipedia


def wp(irc, user, target, msg):
    cmd, title = msg.split(None, 1)
    wikipedia.set_lang('en')

    try:
        page = wikipedia.summary(title, sentences=1)
    except wikipedia.DisambiguationError as e:
        pages = ' | '.join([s.encode('ascii', 'replace')
                            for s in e.options[:10]])
        results = '"%s" may refer to: %s' % (title, pages)
        irc.msg(target, results)
        return
    except wikipedia.PageError as e:
        line = 'No such page: %s' % title.encode('ascii', 'replace')
        irc.msg(target, line)
        return

    page = page.encode('ascii', 'replace')
    irc.msg(target, page)

plugin.add_plugin('^!wp ', wp)
plugin.add_help('!wp', 'Query Wikipedia. Example: !wp ozric tentacles')
