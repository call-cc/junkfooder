import time

import plugin


MAX_LINES = 12


hist_lines = []


def history(irc, user, _target, msg):
    usernick, _ = user.split('!', 1)

    if msg == '!history':
        for timestamp, nick, line in hist_lines:
            result = '%s <%s> %s' % (timestamp, nick, line)
            irc.msg(usernick, result)
    else:
        now = time.strftime('UTC %Y.%m.%d %H:%M:%S',
                            time.gmtime())
        hist_lines.append([now, usernick, msg])
        if len(hist_lines) > MAX_LINES:
            hist_lines.pop(0)


plugin.add_plugin('', history)
plugin.add_help('!history',
                'Sends you the last %s messages on the channel' % MAX_LINES)
