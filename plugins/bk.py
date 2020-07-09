import plugin
import time


def bk(irc, user, target, msg):
    # Sunday is 0th
    menu = ['Big King Chicken',
            'Grill Steakhouse',
            'Big King',
            'Whopper cheese + bacon',
            'Whopper',
            'Deluxe Chicken',
            'Whopper cheese']

    day = int(time.strftime('%w'))
    today = time.strftime("%Y.%m.%d")
    line = 'Menu for %s @ Burger King: %s' % (today, menu[day])
    irc.msg(target, line)


plugin.add_plugin('^!bk\Z', bk)
plugin.add_help('!bk', 'Query Burger King menu')
