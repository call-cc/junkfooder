import plugin
import re
import common


WELCOME_FILE = 'welcome.yaml'


def welcome(irc, user, channel, msg=None):
    try:
        welcomes = common.parse_config('plugins/' + WELCOME_FILE)
    except Exception:
        # fail gracefully, but uninformatively
        return

    for regexp, message in welcomes.iteritems():
        regexp = re.compile(regexp, re.I)
        if re.search(regexp, user):
            line = '[%s] ' % user
            line += message
            irc.msg(channel, line)

plugin.add_plugin('', welcome, 'join')
