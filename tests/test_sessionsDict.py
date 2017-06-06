# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
import unittest
import datetime
from tm import _timeToStr, _timedeltaToStr
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) 

from tm import SessionsDict

class TestTM(unittest.TestCase):
	def setUp(self):
		pass
	def test_logCI(self):
		sd = SessionsDict('./unittest.txt')
		sd.log({})
		self.assertIn('ci', ', '.join(sd.sessions[0].keys()))
		self.assertNotIn('co', ', '.join(sd.sessions[0].keys()))
			
	def test_logCO(self):
		sd = SessionsDict('./unittest.txt')
		sd.log({})
		sd.log({})
		self.assertIn('ci', ', '.join(sd.sessions[0].keys()))
		self.assertIn('co', ', '.join(sd.sessions[0].keys()))

	def test_modifier(self):
		sd = SessionsDict('./unittest.txt')
		sd.log({'a':'b'})
		self.assertIn('a', ', '.join(sd.sessions[0].keys()))
	
	def test_totalOvertime(self):
		sd = SessionsDict('./unittest.txt')
		t0 = datetime.datetime(2017, 05, 01, 8, 00)
		t1 = t0 + datetime.timedelta(hours=10, minutes=15)
		t2 = t0 + datetime.timedelta(hours=8, minutes=15)
		
		sd.sessions.append({'ci': _timeToStr(t0), 'co': _timeToStr(t1)})
		sd.sessions.append({'ci': _timeToStr(t0), 'co': _timeToStr(t2)})
		self.assertEqual(sd.totalOvertime(), datetime.timedelta(0))

if __name__ == '__main__':
	unittest.main()
