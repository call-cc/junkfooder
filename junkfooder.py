#!/usr/bin/env python2


import sys
import glob
import random
import common
import plugin
import os.path
import importlib
from twisted.internet import reactor, protocol
from twisted.words.protocols import irc


CONFIG_FILE = 'junkfooder.yaml'
RECONNECT_TIME = 60


class JunkfooderBot(irc.IRCClient):
    # Yuck!
    # TODO: find a better way
    config = common.parse_config(CONFIG_FILE)['irc']
    nickname = config['nick']
    realname = config['realname']
    username = config['ident']

    def __init__(self):
        # load plug-ins
        plug_dir = os.path.dirname(os.path.abspath(__file__)) + '/plugins/'
        sys.path.append(plug_dir)
        files = glob.glob(plug_dir + '*.py')
        plugs = []
        for f in files:
            name = os.path.basename(f)
            plugs.append(importlib.import_module(name[:-3]))

        self.plugs = plugs

    def connectionMade(self):
        print('Connected')
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        print('Connection lost')
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        print('Online')
        config = self.factory.config['irc']

        nick_password = config.get('nick_password', None)
        if nick_password:
            self.msg('nickserv', 'identify ' + nick_password)

        channel = config['channel']
        key = config.get('channel_key', None)
        self.join(channel, key)

    def privmsg(self, user, target, msg):
        if target != self.nickname:
            plugin.dispatch(self, 'privmsg', user, target, msg)
        else:
            print('MSG: %s' % msg)

    def userJoined(self, user, channel):
        plugin.dispatch(self, 'join', user, channel)

    def userLeft(self, user, channel):
        plugin.dispatch(self, 'part', user, channel)

    def afterCollideNick(self, nickname):
        return nickname + random.randint(100, 999)


class JunkfooderBotFactory(protocol.ClientFactory):
    def __init__(self, config):
        self.config = config

    def buildProtocol(self, addr):
        bot = JunkfooderBot()
        bot.factory = self
        return bot

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.callLater(RECONNECT_TIME, connector.connect)


if __name__ == '__main__':
    config = common.parse_config(CONFIG_FILE)
    bot = JunkfooderBotFactory(config)
    server = config['irc']['server']
    port = config['irc'].get('port', 6667)
    reactor.connectTCP(server, port, bot)
    reactor.run()
