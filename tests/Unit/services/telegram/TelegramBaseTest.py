import unittest
from helpers.Common import *


class TelegramBaseTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_check_job_time_format(self):
        testTrue = check_job_time_format('20190820112233')
        self.assertTrue(testTrue)

        testMonth1 = check_job_time_format('20191320112233')
        self.assertFalse(testMonth1)
        testMonth2 = check_job_time_format('20190020112233')
        self.assertFalse(testMonth2)

        testDay1 = check_job_time_format('20190800112233')
        self.assertFalse(testDay1)
        testDay2 = check_job_time_format('20190832112233')
        self.assertFalse(testDay2)
        testDay3 = check_job_time_format('20190830112233')
        self.assertTrue(testDay3)

        testHour = check_job_time_format('20190820242233')
        self.assertFalse(testHour)

        testMin = check_job_time_format('20190820226160')
        self.assertFalse(testMin)

        testSec = check_job_time_format('20190820222260')
        self.assertFalse(testSec)
