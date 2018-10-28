#
#   DBclass based on SQLite, meant to be used in OscQLite, remote SQLite via OSC
#	15-09-2018:	made it 3.5 compatible
#	27-10-2018: modified for OscQlite
#	28-10-2018: added exec() method
#
import csv, os, random, sqlite3, sys, time, datetime

from functools import partial

showinserts = 0
showupdates = 0
showselects = 0
showexecute = 1

class db(object):
	def __init__( self, dbname = './config.sqlite' ):
		self.DBFILE = dbname
		#self.conn = sqlite3.connect(self.DBFILE, detect_types=sqlite3.PARSE_DECLTYPES,check_same_thread = False )
		self.conn = sqlite3.connect(self.DBFILE, check_same_thread=False)
		#self.conn.row_factory = sqlite3.Row     # allows query results as dictionaries
		self.cur = self.conn.cursor()

	def insert(self, insq, tup):
		if showinserts:print(insq, tup)
		try:
			self.cur.execute(insq, tup)
			self.conn.commit()
			#print self.cur.rowcount
		except sqlite3.Error as e:
			print("Error {}:".format(e.args[0]))

	def update(self, upq):
		if showupdates:print(upq)
		try:
			self.cur.execute(upq)
			self.conn.commit()
			#print self.cur.rowcount
		except sqlite3.Error as e:
			print("Error %s:" % e.args[0])

	def exec(self, exq):
		if showexecute:print(exq)
		try:
			self.cur.execute(exq)
			self.conn.commit()
			return self.cur.rowcount
		except sqlite3.Error as e:
			print("Error %s:" % e.args[0])
			return "Error %s:" % e.args[0]


	def select(self, selq):
		if showselects: print(selq)
		self.cur.execute(selq)
		rows = self.cur.fetchall()
		return rows

	def exists(self, selq):     # returns true or false depending on query
		self.cur.execute(selq)
		rows = self.cur.fetchall()
		if len(rows) == 0:
			result = False
		else:
			result = True
		return result


if __name__ == '__main__':
	conf = db()
	#instr = csdb.select("select * from templates where name ='Single with effects'")
	#print(instr[0]['instrument0'])
	#res = csdb.select('select * from instruments')
	#print(res)
	name = 'PCToos'
	ip = conf.select('select IP from nodes where name="%s" ' % name)
	print(ip[0][0])