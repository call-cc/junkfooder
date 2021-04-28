from unittest import mock
from unittest import TestCase

import urllib

from plugins import covid


class TestCovid(TestCase):

    def setUp(self):
        self.user = 'test_user'
        self.irc = mock.MagicMock()
        self.patch_request = mock.patch('plugins.covid.urllib.request')
        self.mock_request = self.patch_request.start()
        self.patch_open = mock.patch('plugins.covid.open')
        self.mock_open = self.patch_open.start()
        self.patch_remove = mock.patch('plugins.covid.os.remove')
        self.patch_remove.start()

    def tearDown(self):
        self.patch_request.stop()
        self.patch_open.stop()
        self.patch_remove.stop()

    def test_covid_message(self):
        self.mock_open.return_value = open('tests/covid/resources/covidstat.csv', 'r')
        expected_answer = (self.user + ': 2021-04-27 napi adatok | új esetek 1253 | elhunyt 183 | gyógyult 5185 | '
                           'tesztek 11389 | aktív esetek 254103 | lélegeztetőn 753 | oltottak 3679730 | '
                           'napi oltottak 75829 | második oltás 1711723 | második oltás napi 46656 ||')

        covid.covid(self.irc, self.user, 'target', '!covid')
        self.irc.msg.assert_called_with('target', expected_answer)

    def test_url_error(self):
        self.mock_request.urlretrieve.side_effect = urllib.error.HTTPError('url', 'code', 'msg', 'hdrs', 'fp')
        expected_answer = self.user + ': HTTPError, Try again later! (ping skullyka)'

        covid.covid(self.irc, self.user, 'target', '!covid')
        self.irc.msg.assert_called_with('target', expected_answer)
