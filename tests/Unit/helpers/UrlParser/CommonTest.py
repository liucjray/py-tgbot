import unittest
from helpers.Common import dict_get


class CommonTest(unittest.TestCase):

    def setUp(self):
        self.dictionary = {
            'test': {
                'test2': {
                    'test3': 'hello'
                }
            }
        }

    def test_dict_get_by_key(self):
        key = 'test.test2.test3'
        result = dict_get(self.dictionary, key)
        self.assertEqual(result, 'hello')

    def test_dict_get_default(self):
        key = 'NotExistKey'
        result = dict_get(self.dictionary, key, None)
        self.assertEqual(result, None)
