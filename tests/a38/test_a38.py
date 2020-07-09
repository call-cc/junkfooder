from unittest import TestCase

from plugins.a38 import A38
from tests.request_mock import RequestsMock
from tests.resource import suite_resource, content_of


class TestA38(TestCase):
    def test_a38_english_url(self):
        requests_mock = self._minimal_requests_with("a38_en.html")
        a38 = A38(requests=requests_mock)

        a38.fetch_todays_menu()

        self.assertEqual("https://www.a38.hu/en/restaurant", requests_mock.url)

    def test_a38_hungarian_url(self):
        requests_mock = self._minimal_requests_with("a38_en.html")
        a38 = A38(requests=requests_mock, lang="hu")

        a38.fetch_todays_menu()

        self.assertEqual("https://www.a38.hu/hu/etterem", requests_mock.url)

    def test_a38_defaults_to_english(self):
        requests_mock = self._minimal_requests_with("a38_en.html")
        a38 = A38(requests=requests_mock, lang="unknown")

        a38.fetch_todays_menu()

        self.assertEqual("https://www.a38.hu/en/restaurant", requests_mock.url)

    def test_a38_without_menu(self):
        self.assert_message_for(
            "No menu found @ A38",
            "no_menu.html"
        )

    def test_a38_english_menu_list(self):
        self.assert_message_for(
            "Current A38 menu: " + " | ".join([
                "Cauliflower soup",
                "Fried breaded pork with corn rice",
                "Vegetarian: Fried curd cheese with corn rice",
                "Tiramisu"
            ]),
            "a38_en.html")

    def test_a38_hungarian_menu_list(self):
        menu = self.todays_menu_in("a38_hu.html")

        self.assertTrue(
            menu.startswith("Current A38 menu: Karfiolleves")
        )
        self.assertFalse(menu.endswith(" | "))

    def assert_message_for(self, response, resource):
        self.assertEqual(response, self.todays_menu_in(resource))

    def todays_menu_in(self, resource):
        a38 = A38(requests=self._minimal_requests_with(resource))
        return a38.fetch_todays_menu()

    def _minimal_requests_with(self, resource_name):
        return RequestsMock(
            content_of(
                suite_resource(__file__, resource_name)
            )
        )
