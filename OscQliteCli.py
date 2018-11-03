"""

OscQliteCli: client fpr remote SQLite via OSC

by:			zappfinger (Richard van Bemmelen)
version:	1.0
date:		27-10-2018

"""

from pythonosc import dispatcher
from pythonosc import osc_server, udp_client
import threading
from queue import Queue
from commands import *
import json

"""
	enter the name of the SQLite machine to connect to
"""
##########################
name = 'Pi3B+'
#name = 'Acer'
##########################
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

	def checkQ(self):
		while not q.empty():
			print(q.get())

	def send(self, cmd):
		self.client.send_message("/command", cmd)
		reptext = json.loads(q.get())
		if type(reptext)==list and len(reptext)>1:
			for txt in reptext:
				print(txt)
		else:
			print(reptext)
		time.sleep(1)

	def sendSQL(self, cmd):
		self.client.send_message("/SQLcommand", cmd)
		time.sleep(1)

if __name__ == "__main__":
	def worker1():
		serv = server('0.0.0.0', 8889)
		print("OsCommandCli serving on {}".format(serv.server.server_address))
		serv.server.serve_forever()

	def worker2():
		clint = client(otherIP, 8889)
		while 1:
			cmd = input('Enter command, (SQL command starts with "SQL@") : ')
			if 'SQL@' in cmd:
				try:
					clint.sendSQL(cmd.split('@')[1])
				except:
					print('Please enter SQL command in the format "SQL@select * from table"')
			else:
				clint.send(cmd)
			#time.sleep(1)
			clint.checkQ()

	thread_list = []
	thread1 = threading.Thread(target=worker1)
	thread_list.append(thread1)
	thread1.start()
	time.sleep(1)
	thread2 = threading.Thread(target=worker2)
	thread_list.append(thread2)
	thread2.start()

while 1:
	time.sleep(.5)	# uses less CPU than pass
