# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from os import sys, path
import datetime
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) 

from tm import Session 

class TestTM(unittest.TestCase):
	def setUp(self):
		pass

	def test_sessionToSessionLineToSession(self):
		t0 = datetime.datetime(2017, 05, 01, 8, 10)
		t8 = t0 + datetime.timedelta(hours=8)
		s = Session(ci=t0, co=t8, modifiers={'holiday':True})
		line = s.toLine()
		self.assertEqual(line, Session.fromLine(line).toLine())

	def test_sessionFromSessionLine_comment(self):
		self.assertIsNone(Session.fromLine('#a:b\n'))

if __name__ == '__main__':
	unittest.main()
