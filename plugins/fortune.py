import plugin
import subprocess


def fortune(irc, user, target, msg):
    try:
        output = subprocess.check_output('fortune').decode()
    except Exception as e:
        irc.msg(target, 'Error executing "fortune":' % e)
    lines = output.split('\n')
    # pop: Remove last empty element
    lines.pop()
    for line in lines:
        irc.msg(target, line)


plugin.add_plugin('^!fortune\Z', fortune)
plugin.add_help('!fortune', 'Provide a random fortune')
