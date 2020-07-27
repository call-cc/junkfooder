import plugin
import requests
import re


def wttr(irc, user, target, msg):
    nick = user.partition('!')[0]
    items = msg.split(' ')
    if len(items) <= 1:
        city = "Budapest"
    else:
        city = "+".join(items[1:])

    reply = Wttr().get_wttr(city, nick)
    irc.msg(target, reply)


plugin.add_plugin('^(!wttr)( .*)?$', wttr)
plugin.add_help('!wttr',
                'Fancy weather forecast using wttr.it Example: !wttr Budapest')


class Wttr:
    def __init__(self):
        self.nick = ""
        self.wttr = ""

    def get_wttr(self, city, nick):
        self.nick = nick
        req = requests.get("http://wttr.in/" + city)
        self.wttr = req.text.split('\n')
        response = self.__format_response()
        return response

    def __format_response(self):
        if self.wttr[0].startswith("ERROR"):
            response = self.nick + ": " + self.wttr[0] + " :("
        else:
            location = self.__get_location()
            ansi_content = '\n'.join(self.wttr[2:7] + [location])
            response = Wttr.change_ansi_to_irc(ansi_content)
        return response

    def __get_location(self):
        if self.wttr[-4].startswith("Location:"):
            loc = self.wttr[-4]
        else:
            loc = "\n".join(self.wttr[-6:-2])
        return loc

    @staticmethod
    def change_ansi_to_irc(strcontent):
        strcontent_resetcolor_changed = re.sub(r'\033\[\dm', '\x03', strcontent)
        all_ansi_colors = set(re.findall(r'(\033[^m]*m)', strcontent_resetcolor_changed))
        for color in all_ansi_colors:
            irc_color = Wttr.change_ansi_graph_to_irc(color)
            strcontent_resetcolor_changed = strcontent_resetcolor_changed.replace(color, irc_color)
        return strcontent_resetcolor_changed

    @staticmethod
    def change_ansi_graph_to_irc(ansi_graphic_string):
        splitted_ansi_graphic = ansi_graphic_string.split(";")
        ansi_color = splitted_ansi_graphic[2].replace("m", "")
        irc_color = Wttr.convert_colors(ansi_color)
        return "\x03" + irc_color

    @staticmethod
    def convert_colors(ansi_color):
        for ansi_color_group, irc_color in Wttr.ansi_colors_in_irc().items():
            if ansi_color in ansi_color_group:
                return irc_color
        return "00"

    @staticmethod
    def ansi_colors_in_irc():
        return {
            ("15"): "00",
            ("21"): "02",
            ("202"): "04",
            ("154", "190", "226", "220", "228"): "08",
            ("46", "82", "118"): "09",
            ("45", "48", "47"): "10",
            ("27", "33", "39", "111"): "12",
            ("214", "208"): "13",
            ("250", "251", "240", "255"): "15"
        }
