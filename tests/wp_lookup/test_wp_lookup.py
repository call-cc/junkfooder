from unittest import mock
from unittest import TestCase

import wikipedia

from plugins import wp_lookup


NORMAL_SEARCH_SENTENCE = 'Python is an interpreted, high-level, general-purpose programming language.'
NORMAL_SEARCH_URL = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

DISAMBIGUATION_OPTIONS = [
    'Challenger Deep',
    'Deep Creek (Appomattox River tributary)',
    'Deep Creek (Great Salt Lake)',
    'Deep Creek (Mahantango Creek tributary)',
    'Deep Creek (Mojave River tributary)',
    'Deep Creek (Pine Creek tributary)',
    'Deep Creek (Soque River tributary)',
    'Deep Creek (Texas)',
    'Deep Creek (Washington)',
    'Deep River (Indiana)',
    'Deep River (Iowa)',
    'Deep River (North Carolina)',
    'Deep River (Washington)',
    'Deep Voll Brook'
]
DISAMBIGUATION_ANSWER = (
    '"The Deep" may refer to: Challenger Deep | Deep Creek (Appomattox River tributary) | '
    'Deep Creek (Great Salt Lake) | Deep Creek (Mahantango Creek tributary) | Deep Creek (Mojave River tributary) | '
    'Deep Creek (Pine Creek tributary) | Deep Creek (Soque River tributary) | Deep Creek (Texas) | '
    'Deep Creek (Washington) | Deep River (Indiana)'
)


class TestWikipediaLookup(TestCase):

    def setUp(self):
        self.irc = mock.MagicMock()
        self.patch_wikipedia_summary = mock.patch('plugins.wp_lookup.wikipedia.summary')
        self.mock_wikipedia_summary = self.patch_wikipedia_summary.start()
        self.patch_wikipedia_page = mock.patch('plugins.wp_lookup.wikipedia.page')
        self.mock_wikipedia_page = self.patch_wikipedia_page.start()

    def tearDown(self):
        self.patch_wikipedia_summary.stop()
        self.patch_wikipedia_page.stop()

    def test_normal_search_and_result(self):
        self.mock_wikipedia_summary.return_value = NORMAL_SEARCH_SENTENCE
        mock_page = mock.MagicMock()
        mock_page.url = NORMAL_SEARCH_URL
        self.mock_wikipedia_page.return_value = mock_page

        expected_answer = '%s For more: %s' % (NORMAL_SEARCH_SENTENCE, NORMAL_SEARCH_URL)
        wp_lookup.wikipedia_lookup(self.irc, 'user', 'target', '!wp Python programming language')

        self.irc.msg.assert_called_with('target', expected_answer)

    def test_disambiguation(self):
        self.mock_wikipedia_summary.side_effect = wikipedia.DisambiguationError('dummy', DISAMBIGUATION_OPTIONS)
        wp_lookup.wikipedia_lookup(self.irc, 'user', 'target', '!wp The Deep')
        expected_answer = DISAMBIGUATION_ANSWER

        self.irc.msg.assert_called_with('target', expected_answer)

    def test_no_such_page(self):
        self.mock_wikipedia_summary.side_effect = wikipedia.PageError('dummy')
        wp_lookup.wikipedia_lookup(self.irc, 'user', 'target', '!wp GTFO')
        expected_answer = 'No such page: GTFO'

        self.irc.msg.assert_called_with('target', expected_answer)
