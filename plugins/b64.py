import plugin
import base64


def b64e(irc, user, target, msg):
    cmd, text = msg.split(None, 1)

    result = base64.b64encode(text)
    irc.msg(target, 'Base64: %s ' % result)
    return

plugin.add_plugin('^!base64 ', b64e)
plugin.add_help('!base64', 'Base64 encodes the argument. Example: !base64 foo')
