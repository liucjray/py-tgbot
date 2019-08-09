import unittest
from helpers.UrlParser import get_qs


class UrlParserTest(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhsot/?a=aaa&q=qqq'

    def test_get_qs_get_value_by_key(self):
        result = get_qs(self.url, 'a', None)
        self.assertEqual(result, 'aaa')

    def test_get_qs_default(self):
        result = get_qs(self.url, 'z', None)
        self.assertEqual(result, None)

    def test_get_qs_get_value_no_default(self):
        result = get_qs('http://localhost/?a=&b=', 'a')
        self.assertEqual(result, None)
