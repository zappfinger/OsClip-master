"""

Client: client for remote SQLite via OSC

by:			zappfinger (Richard van Bemmelen)
version:	1.0
date:		04-11-2018

"""

from pythonosc import dispatcher
from pythonosc import osc_server, udp_client
import threading
from queue import Queue
import time, sys
import json
from DBclass import *

"""
	enter the name of the SQLite machine to connect to
"""
##########################
name = 'Pi3B+'
#name = 'Acer'
##########################

#	get config from local database
conf = db()
otherIP = conf.select('select IP from nodes where name="%s" ' % name)[0][0]

q = Queue()

class server():
	def __init__(self, ip, port):
		self.dispatcher = dispatcher.Dispatcher()
		self.dispatcher.map("/reply", self.reply_handler, "")
		self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)

	def reply_handler(self, unused_addr, args, reptext):
		# get the reply and send it to the client via queue
		#print(reptext)
		q.put(reptext)



class client():
	def __init__(self, ip, port):
		self.client = udp_client.SimpleUDPClient(ip, port)
		self.start()	# start the server part

	"""Call this to get data sent back to us"""
	def checkQ(self):
		while not q.empty():
			return eval(q.get())

	"""Send normal command (like 'ls' or 'dir') and get reply"""
	def send(self, cmd):
		self.client.send_message("/command", cmd)
		reptext = json.loads(q.get())
		if type(reptext)==list and len(reptext)>1:
			for txt in reptext:
				print(txt)
		else:
			print(reptext)
		time.sleep(1)

	"""Send SQL command, then call checkQ() to get the reply"""
	def sendSQL(self, cmd):
		self.client.send_message("/SQLcommand", cmd)
		time.sleep(1)

	def worker1(self):
		serv = server('0.0.0.0', 8889)
		print("SQLiteClient clienting on {}".format(serv.server.server_address))
		serv.server.serve_forever()

	def start(self):
		thread_list = []
		thread1 = threading.Thread(target=self.worker1)
		thread_list.append(thread1)
		thread1.start()
		time.sleep(1)

if __name__ == "__main__":
	"""
	Example of how to use this class
	"""
	#	connect to the other side
	clint = client(otherIP, 8889)
	#	send SQL command to be executed there
	clint.sendSQL('select * from employees')
	#	get the reply
	try:
		ret = clint.checkQ()
		for rec in ret:
			print(rec)
		time.sleep(1)
	except:
		sys.exit("no reply. Is oscommand running on the other side?")


	#	send a normal command and get the reply
	clint.send('ls')
	ret = clint.checkQ()
	print(ret)