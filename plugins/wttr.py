import plugin
import requests


def wttr(irc, user, target, msg):
    items = msg.split(' ')
    nick = user.partition('!')[0]
    # return if there are no choices to choose from
    if len(items) <= 1:
        item = nick +": Give me a city!"
        irc.msg(target, item)
        return
    print(items)
    
    req=requests.get("http://wttr.in/"+items[1])
    content = req.text.split('\n')
    
    
    if content[0].startswith("ERROR"):
        item = nick +": Can't find the city. :("
    else:
        item = '\n'.join(content[2:7])
    
    irc.msg(target, item)

plugin.add_plugin('^!wttr ', wttr)
plugin.add_help('!wttr',
                'Fancy weather forecast using wttr.it')

def colorconvert():
    #256 to irc
    pass
