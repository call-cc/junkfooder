import plugin
import base64


def b64(irc, user, target, msg):
    cmd, text = msg.split(None, 1)

    # Lazy
    if cmd == '!b64d':
        result = base64.b64decode(text)
    else:
        result = base64.b64encode(text)
    irc.msg(target, 'Base64: %s ' % result)
    return

plugin.add_plugin('^!(base64|b64e?|b64d) ', b64)
plugin.add_help('!base64', 'Base64 encodes the argument. Example: !base64 foo')
plugin.add_help('!b64d', 'Base64 decodes the argument. Example: !b64d Zm9v')
