import re


plugins = []
help = []


def add_plugin(regexp, func, event='privmsg'):
    plugins.append((event, regexp, func))


def dispatch(irc, event, user, target, msg=''):
    for trigger, regexp, func in plugins:
        r = re.compile(regexp, re.I)
        if re.search(r, msg) and event == trigger:
            func(irc, user, target, msg)


def add_help(string, message):
    help.append((string, message))


def get_help(string=None):
    if string is None:
        return ', '.join(sorted(map(lambda x: x[0], help)))
    else:
        for cmd, doc in help:
            if cmd == string:
                line = "%s: %s" % (cmd, doc)
                return line

        return "No help for %s" % string
