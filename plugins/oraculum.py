import plugin
import pickle
import re


FACT_FILE = 'facts.dat'


def oraculum_q(irc, user, target, msg):
    if re.search('^\? .+', msg):
        cmd, topic = msg.split(' ', 1)
        try:
            with open(FACT_FILE, 'rb') as f:
                facts = pickle.load(f)
                fact = facts.get(topic, None)
                if fact:
                    line = '%s: %s' % (topic, fact)
                    irc.msg(target, line)
                else:
                    irc.msg(target, 'No such fact: %s' % topic)
        except Exception:
            # TODO: error handling
            return


# plugin.add_plugin('^![+-] ', oraculum)
plugin.add_plugin('^\? .+', oraculum_q)
