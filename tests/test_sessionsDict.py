# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
import datetime
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

if __name__ == '__main__':
	unittest.main()
