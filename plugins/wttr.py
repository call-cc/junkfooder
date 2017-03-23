import plugin
import requests
import re


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
        item = nick +": content[0] :("
    else:
        item = '\n'.join(content[2:7])
        item = change_ansi_to_irc(item)
    
    irc.msg(target, item)

plugin.add_plugin('^!wttr ', wttr)
plugin.add_help('!wttr',
                'Fancy weather forecast using wttr.it Example: !wttr Budapest')

def change_ansi_to_irc(strcontent):
    # reset color
    strcontent = re.sub('\\033\[\dm','\x03' , strcontent)
    ansi_colors = re.findall(r'(\033[^m]*m)', strcontent) 
    for color in ansi_colors:
        strcontent = strcontent.replace(color,change_ansi_graph_to_irc(color))
   
    print strcontent
    return strcontent

def change_ansi_graph_to_irc(ansi_graphic_string): 
    ansicolor = ansi_graphic_string.split(";")
    ansicolor = ansicolor[2].replace("m","")
    irccolor = convert_colors(ansicolor)

    print ansi_graphic_string, ansicolor, irccolor
    return "\x03" + irccolor

def convert_colors(ansicolor):
    for k,v in ansi_colors_in_irc().items():
        if ansicolor in k:
            return v
    return "00"

def ansi_colors_in_irc():
    return {
        ("15") : "00",
        ("21") : "02",
        ("202") : "04",
        ("154","190", "226", "220", "228")  : "08",
        ("46", "82", "118") : "09",
        ("45","48","47") :"10",
        ("27", "33", "39", "111") : "12",
        ("214", "208") : "13",
        ("250", "251", "240", "255") : "15"
        }
