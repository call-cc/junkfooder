import plugin
from sys import version_info as vi


def j_version(irc, user, target, msg):
    v1 = vi.major
    v2 = vi.minor
    v3 = vi.micro
    irc.msg(target, "I'm running on Python {}.{}.{}".format(v1, v2, v3))


plugin.add_plugin('^!ver\Z', j_version)
plugin.add_help('!ver', 'Show Python version')
