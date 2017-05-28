# -*- coding: utf-8 -*-
"""

@author: nicolas
"""
from __future__ import unicode_literals
import argparse
import os
import sys
import datetime
import time
import pdb

# --- Define constants --- 
LUNCH_DURATION = datetime.timedelta(minutes=45)

def _sessionFromSessionLine(sessionLine):
	session = {}
	if sessionLine.strip().startswith('#'):
		return None
	else:
		for piece in sessionLine.strip().split(','):
			label, data = piece.split(':')
			session[label.strip()] = data.strip()

		return session

def _sessionLineFromSession(session):
	sessionLine = ""
	meta = [m for m in session.items()]
	s = ', '.join('%s:%s' % m for m in meta)
	return s+"\n"

def _workingTimeFromSession(session):
	date_ci = _strToTime(session['ci']) 
	date_co = _strToTime(session['co'])
	timeWorked = date_co - date_ci - LUNCH_DURATION 
	hours, remainder = divmod(timeWorked.seconds, 3600)
	minutes, seconds = divmod(remainder, 60)
        return "%dh%02d" % (hours, minutes) 

def timeStr():
	return datetime.datetime.now().strftime("%G%m%d/%H-%M-%S")

def _timeToStr(time):
	return time.strftime("%G%m%d/%H-%M-%S")

def _strToTime(string):
	return datetime.datetime.strptime(string, "%Y%m%d/%H-%M-%S")

class SessionsDict(object):
	def __init__(self, path='./tm.txt'):
		self.sessions = [] 
		self.path = path
		if os.path.exists(self.path):
			try:
				with open(self.path, 'r') as f:
					lines = [l.strip() for l in f if l]
					for l in lines:
						self.sessions.append(_sessionFromSessionLine(l))
			except:
				print(sys.exc_info()[0])
		
	def log(self, special_days):
		if not self.sessions:
			self.logCI()
		else:
			if 'co' not in self.sessions[-1]:
				self.logCO()
			else:
				self.logCI()

		# adds modifiers
		for  key,value in special_days.items():
			if (value):
				self.sessions[-1][key]='true'

	def logCI(self):
		currentDate = datetime.datetime.now()
		self.sessions.append({'ci': _timeToStr(currentDate)})
		print("Logged check-in at "+ self.sessions[-1]['ci'])

	def logCO(self):
		currentDate = datetime.datetime.now()
		self.sessions[-1]['co'] = _timeToStr(currentDate)
                
		print("Logged check-out at " + self.sessions[-1]['co'])
		print("Total working time today: " + _workingTimeFromSession(self.sessions[-1]))

	def write(self):
		try:
			with open(self.path, 'w') as f:
				for session in self.sessions:
					s = _sessionLineFromSession(session)
					f.write(s)
		except:
			print("hihi")

def main(arg):
	parser = argparse.ArgumentParser(description='Time Manager')
	parser.add_argument('--path', help="path to log file", required=True)
	parser.add_argument('--holiday', help="when the day is actually a holiday",
            action="store_true")
        parser.add_argument('--half-day', help="when working half a day",
            action="store_true")
	args = parser.parse_args()
	path = args.path
	sd = SessionsDict(path)
	sd.log({'holiday':args.holiday, 'half-day':args.half_day})
	sd.write()


if __name__ == '__main__':
	main(sys.argv)

