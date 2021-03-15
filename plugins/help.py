import re

import plugin


def help(irc, _user, target, msg):
    if re.search('^!help\Z', msg):
        doc = 'Available commands: %s' % plugin.get_help()
        irc.msg(target, doc)
    elif re.search('^!help !.+', msg):
        cmd, plug = msg.split(None, 1)
        doc = plugin.get_help(plug)
        irc.msg(target, doc)
    else:
        irc.msg(target, "Usage example: !help !wp")


plugin.add_plugin('^!help', help)
plugin.add_help('!help', 'Help command. Example: !help !wp')
