import unittest
from helpers.Encoder import to_md5


class EncoderTest(unittest.TestCase):

    def test_english(self):
        result = to_md5('test')
        self.assertEqual(result, '098f6bcd4621d373cade4e832627b4f6')

    def test_chinese(self):
        result = to_md5('測試')
        self.assertEqual(result, 'b7dfcd49856b273e35b9504a921c8078')

    def test_number(self):
        result = to_md5('123')
        self.assertEqual(result, '202cb962ac59075b964b07152d234b70')
