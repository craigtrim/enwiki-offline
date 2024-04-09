# -*- coding: utf-8 -*-


import unittest

from enwiki_offline import EnwikiOfflineAPI


class TestExistsFunction(unittest.TestCase):

    def setUp(self) -> None:
        self.api = EnwikiOfflineAPI()
        return super().setUp()

    def tearDown(self) -> None:
        self.api = None
        return super().tearDown()

    def test_exists(self) -> None:
        self.assertTrue(self.api.exists('Secamonopsis madagascariensis'))
        self.assertTrue(self.api.exists('john kao'))
        self.assertFalse(self.api.exists('not going to find this anywhere'))

    def test_is_ambiguious(self) -> None:
        self.assertTrue(self.api.is_ambiguous('abba'))
        self.assertFalse(self.api.is_ambiguous('john kao'))

    def test_title(self) -> None:
        self.assertEqual(
            self.api.titles('abba')[0],
            'https://en.wikipedia.org/wiki/ABBA')

        self.assertEqual(
            len(self.api.titles('abba')), 7)

        self.assertEqual(
            self.api.titles('Secamonopsis madagascariensis'),
            ['https://en.wikipedia.org/wiki/Secamonopsis_madagascariensis'])

        self.assertIsNone(
            self.api.titles('asdfjkasdjf'*23))


if __name__ == '__main__':
    unittest.main()
