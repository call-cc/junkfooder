import plugin
import re
import time
import common


WELCOME_FILE = 'welcome.yaml'
WELCOME_TIME = 4 * 3600

# store timestamps for welcomes
memory = {}


def welcome(irc, user, channel, msg=None):

    try:
        welcomes = common.parse_config('plugins/' + WELCOME_FILE)
    except Exception:
        # fail gracefully, but uninformatively
        return

    for regexp, message in welcomes.iteritems():
        regexp = re.compile(regexp, re.I)
        timestamp = memory.get(regexp, 0)
        if re.search(regexp, user) and timestamp < time.time() - WELCOME_TIME:
            line = '[%s] ' % user
            line += message
            irc.msg(channel, line)
            memory[regexp] = time.time()

plugin.add_plugin('', welcome, 'join')
