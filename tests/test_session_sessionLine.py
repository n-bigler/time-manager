# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) 

from tm import Session 

class TestTM(unittest.TestCase):
    def setUp(self):
        pass

#    def test_sessionToSessionLineToSession(self):
#        self.assertEqual(Session.fromLine(
#            _sessionLineFromSession({'a':'b', 'c':'d'})), {'a':'b', 'c':'d'})

    def test_sessionFromSessionLine_comment(self):
        self.assertIsNone(Session.fromLine('#a:b\n'))

if __name__ == '__main__':
    unittest.main()
