import plugin
import random


def eightball(irc, user, target, msg):
    items = msg.split(' ')
    
    nick = user.partition('!')[0]

    if len(items) <= 1: #no questions to answer...
        irc.msg(target, nick + ': Please, ask your question!')
        return
     
    answers = [
    'It is certain',
    'It is decidedly so',
    'Without a doubt',
    'Yes definitely',
    'You may rely on it',
    'As I see it, yes',
    'Most likely',
    'Outlook good',
    'Yes',
    'Signs point to yes',
    'Reply hazy try again',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again',
    'Don\'t count on it',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Very doubtful',
    ]

    rnd = random.randint(0, len(answers) - 1)
    irc.msg(target, nick + ': ' + answers[rnd])

plugin.add_plugin('^!8ball ', eightball)
plugin.add_help('!8ball',
                'The Magic 8-Ball is a toy used for fortune-telling or seeking' +
                ' advice, developed in the 1950s. Example: !8ball Will I have' + 
                ' a great day?')
