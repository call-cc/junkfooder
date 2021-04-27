import urllib.request
import os
import plugin
import csv


def covid(irc, user, target, msg):
    nick = user.partition('!')[0]

    url = 'https://docs.google.com/spreadsheets/d/1e4VEZL1xvsALoOIq9V2SQuICeQrT5MtWfBm32ad7i8Q/export?format=csv'
    filename = '/tmp/covidstat.csv'
    try:
        urllib.request.urlretrieve(url, filename)
    except urllib.error.HTTPError:
        msg = "HTTPError, Try again later! (ping skullyka)"
    else:
        data = []
        with open(filename, 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                pass
            data = row

        msg = create_msg(data)

        os.remove(filename)

    irc.msg(target, nick + ': ' + msg)


def create_msg(data):
    date = data[0]
    new_cases = data[2]
    new_passed_away = data[17]
    new_healed = data[18]
    new_tests = data[15]
    active_cases = data[11]
    ventillator = data[20]
    vaccinated = data[32]
    new_vaccinated = data[33]
    second_vaccne = data[35]
    new_second_vaccine = data[36]

    msg = date + ' napi adatok'
    msg += ' | új esetek ' + new_cases
    msg += ' | elhunyt ' + new_passed_away
    msg += ' | gyógyult ' + new_healed
    msg += ' | tesztek ' + new_tests
    msg += ' | aktív esetek ' + active_cases
    msg += ' | lélegeztetőn ' + ventillator
    msg += ' | oltottak ' + vaccinated
    msg += ' | napi oltottak ' + new_vaccinated
    msg += ' | második oltás ' + second_vaccne
    msg += ' | második oltás napi ' + new_second_vaccine + ' ||'

    return msg


plugin.add_plugin('^!covid', covid)
plugin.add_help('!covid',
                'Hungarian covid stats')
