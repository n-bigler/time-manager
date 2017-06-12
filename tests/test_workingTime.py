# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import datetime
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) 

from tm import Session, _timeToStr


class TestTM(unittest.TestCase):
    def setUp(self):
        pass
    def test_8(self):
        t0 = datetime.datetime(2017, 05, 01, 8, 10)
        t8 = t0 + datetime.timedelta(hours=8)
        self.assertEqual(Session(ci=_timeToStr(t0), co=_timeToStr(t8)).timeWorked(),
			datetime.timedelta(hours=7, minutes=15)) 

if __name__ == '__main__':
    unittest.main()
