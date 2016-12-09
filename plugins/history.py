import plugin


hist_lines = []


def history(irc, user, target, msg):
    usernick, _ = user.split('!', 1)

    if msg == '!history':
        for nick, line in hist_lines:
            result = '<%s> %s' % (nick, line)
            irc.msg(usernick, result)
    else:
        hist_lines.append([usernick, msg])
        if len(hist_lines) > 10:
            hist_lines.pop(0)

plugin.add_plugin('', history)
plugin.add_help('!history', 'Sends you the last 10 messages on the channel')
