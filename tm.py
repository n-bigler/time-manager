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
import math
import pdb

# --- Define constants --- 
LUNCH_DURATION = datetime.timedelta(minutes=45)
WORKING_HOURS = datetime.timedelta(hours=8, minutes=30)

class IncompleteSessionException(Exception):
	""" Error handling the incomplete session case
		
		Will be raised whenever a session not containing both ci and co is 
		passed to a function requiring a complete session.

	"""
	pass

class InvalidLineException(Exception):
	pass


# def _workingTimeFromSession(session):
# 	""" Computes the time worked during a session
# 
# 	Will be dependent on the LUNCH_DURATION constant
# 	
# 	Args:
# 		session (dict): The session. Right now, this will sadly fail in case
# 			there is no checkout time.
# 			
# 	Returns:
# 		datetime.timedelta: The time worked during the session
# 	"""
# 	if session.co is None or session.ci is None:
# 		raise IncompleteSessionException
# 
# 	date_ci = _strToTime(session.ci) 
# 	date_co = _strToTime(session.co)
# 	timeWorked = date_co - date_ci - LUNCH_DURATION 
# 	return timeWorked 

def _timedeltaToStr(timedelta):
	""" Creates a string description of a timedelta
	
	CURRENTLY ONLY WORKS PROPERLY FOR TIMEDELTA BELOW +- 1 DAY

	The strings generated has the for hh:mm, for example, for a timedelta
	where hours=2 and minutes=10, it would generate 02:10. The function also
	handles negative timedelta by appending a '-' in from (for example,
	-02:10 for the case defined above).

	Args:
		timedelta (datetime.timedelta): The timedelta to be displayed as a
			string.

	Returns:
		str: A string representation of the timedelta, in the form hh:mm

	"""		
	seconds = math.fabs(timedelta.total_seconds())
	hours, remainder = divmod(seconds, 3600)
	minutes = math.floor(remainder/60)
	if (timedelta < datetime.timedelta(0)):
		signStr = "-"
	else:
		signStr = ""
	return signStr+"%d:%02d" % (hours, minutes)

def _overtimeFromTimeWorked(timeWorked):
	""" Computes the overtime based on the time worked in a day

	This will depend on the constant WORKING_HOURS

	Args:
		timeWorked (datetime.timedelta): The time worked in the day.
	
	Returns:
		datetime.timedelta: The overtime done.
	"""
	
	return timeWorked-WORKING_HOURS

def timeStr():
	""" Generate a string representation of the current time

	Returns:
		str: A string representation of the current time
	"""
	return datetime.datetime.now().strftime("%G%m%d/%H-%M-%S")

def _strToTime(string):
	""" Parse a string into a datetime

		The string needs to have been generated by ``_timeToStr()``.
	
		Returns:
			datetime.datetime: A datetime representation of the parsed string
	"""

	return datetime.datetime.strptime(string, "%Y%m%d/%H-%M-%S")

def _timeToStr(time):
	""" Generate a string representation of a certain time
	
		Args:
			time (datetime.datetime): The time to be converted to a string
	
		Returns:
			str: A string representation of ``time`` 
	"""
	return time.strftime("%G%m%d/%H-%M-%S")

class Session(object):
	def __init__(self, ci, co=None, modifiers={}):
		self.ci = ci
		self.co = co
		self.modifiers = modifiers

	@classmethod
	def fromLine(cls, line):
		""" Parse a session line into a session

			A session line is a string of the form:
			label1:data1, label2:data2, label3:data3

			Args:
				sessionLine (str): The line to be parsed

			Returns:
				dict: A dictionary containing every label and data contained in the
					line.
		"""
		modifiers = {}
		co = None
		ci = None
		if line.strip().startswith('#'):
			return None
		else:
			for piece in line.strip().split(','):
				label, data = piece.split(':')
				if label.strip() == 'co':
					co = _strToTime(data.strip())
				if label.strip() == 'ci':
					ci = _strToTime(data.strip())
				modifiers[label.strip()] = data.strip()
					
		if ci is None:
			raise InvalidLineException
	
		return cls(ci, co, modifiers)

	def isModifier(self, modifier):
		if modifier in self.modifiers:
			return self.modifiers[modifier] 

	def timeWorked(self):
		""" Computes the time worked during a session
	
		Will be dependent on the LUNCH_DURATION constant
		
		Args:
			session (dict): The session. Right now, this will sadly fail in case
				there is no checkout time.
				
		Returns:
			datetime.timedelta: The time worked during the session
		"""
		if self.co is None or self.ci is None: 
			raise IncompleteSessionException
	
		date_ci = self.ci 
		date_co = self.co
		timeWorked = date_co - date_ci - LUNCH_DURATION 
		return timeWorked 

	def toLine(self):
		""" Generate a sessionLine from a session

		A session line is a string of the form:
		label1:data1, label2:data2, label3:data3

		Args:
			session (dict): A dictionary of the session. Should contain only
				strings as values. Although it could contain any label, it will
				usually at least have 'ci' and usually 'co' 
		Returns:
			str: A string representation of the session

		"""
		d = {'ci': _timeToStr(self.ci)}

		for k,v in self.modifiers.items():
			d[k] = v
			
		if self.co is not None:
			d['co'] = _timeToStr(self.co)

		sessionLine = ""
		meta = [m for m in d.items()]
		s = ', '.join('%s:%s' % m for m in meta)
		return s+"\n"

	def hasCO(self):
		if self.co is not None:
			return True
		return False

	def addModifier(self, mod, val):
		self.modifiers[mod]=val

class SessionsDict(object):
	def __init__(self, path='./tm.txt'):
		self.sessions = [] 
		self.path = path
		if os.path.exists(self.path):
			try:
				with open(self.path, 'r') as f:
					lines = [l.strip() for l in f if l]
					for l in lines:
						self.sessions.append(Session.fromLine(l))
			except NameError as e:
				print(sys.exc_info()[0])
				print(str(e))
		
	def log(self, special_days):
		if not self.sessions:
			self.logCI()
		else:
			if not self.sessions[-1].hasCO():
				self.logCO()
			else:
				self.logCI()

		# adds modifiers
		for  key,value in special_days.items():
			if (value):
				self.sessions[-1].addModifier(key, 'true')

	def logCI(self):
		currentDate = datetime.datetime.now()
		self.sessions.append(Session(ci=currentDate))
		print("Logged check-in at "+ _timeToStr(self.sessions[-1].ci))

	def logCO(self):
		currentDate = datetime.datetime.now()
		self.sessions[-1].co = currentDate
                
		print("Logged check-out at " + _timeToStr(self.sessions[-1].co))
		timeWorked = self.sessions[-1].timeWorked()
		print("Total working time today: " 
				+ _timedeltaToStr(timeWorked))
		overtime = _overtimeFromTimeWorked(timeWorked)
		if (overtime > datetime.timedelta(0)):
			print("You made " + _timedeltaToStr(overtime) + " of overtime today")

	def write(self):
		try:
			with open(self.path, 'w') as f:
				for session in self.sessions:
					f.write(session.toLine())
		except IOError as e:
			print("Can't write to file.")
			print(str(e))
	
	def totalOvertime(self):
		overtime=datetime.timedelta(0)
		for s in self.sessions:
			try:
				worked = s.timeWorked()
			except IncompleteSessionException:
				worked = WORKING_HOURS 
			except Exception as e:
				print(str(e))
			if s.isModifier('holiday'):
				overtime += worked
			else:
				overtime += _overtimeFromTimeWorked(worked)	
		return overtime
			

def main(arg):
	parser = argparse.ArgumentParser(description='Time Manager')
	parser.add_argument('--path', help="path to log file", required=True)
	parser.add_argument('--holiday', help="when the day is actually a holiday",
            action="store_true")
	parser.add_argument('--half-day', help="when working half a day",
            action="store_true")
	parser.add_argument('--overtime', help="compute overtime (does not check in or out)",
			action="store_true")
	args = parser.parse_args()

	path = args.path
	sd = SessionsDict(path)
	if (args.overtime):
		ot = sd.totalOvertime()
		print("Total overtime: " + _timedeltaToStr(ot))
	else:	
		sd.log({'holiday':args.holiday, 'half-day':args.half_day})
		sd.write()


if __name__ == '__main__':
	main(sys.argv)

