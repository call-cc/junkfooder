import random

import plugin


def decide(irc, user, target, msg):
    items = msg.split(' ')
    # return if there are no choices to choose from
    if len(items) <= 2:
        return

    # remove empty "items"
    items = [item for item in items if item != '']
    # skip the first item, which is '!decide '
    rnd = random.randint(1, len(items) - 1)
    item = items[rnd]
    item = item.lstrip().rstrip()
    irc.msg(target, item)


plugin.add_plugin('^!decide ', decide)
plugin.add_help('!decide',
                'Randomly select an option. Example: !decide tea coffee beer')
