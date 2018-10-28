"""

OsCommand: remote command server

by:			zappfinger (Richard van Bemmelen)
version:	1.0
date:		28-10-2018

"""

from pythonosc import dispatcher
from pythonosc import osc_server, udp_client
import threading
from queue import Queue
from commands import *
from subprocess import Popen, PIPE, STDOUT
import json

"""
	enter the name of the SQLite client machine to connect to
"""
##########################
name = 'Macbook'
##########################
conf = db()
otherIP = conf.select('select IP from nodes where name="%s" ' % name)[0][0]

q = Queue()

class server():
	def __init__(self, ip, port):
		self.dispatcher = dispatcher.Dispatcher()
		self.dispatcher.map("/command", self.command_handler, "")
		self.dispatcher.map("/SQLcommand", self.SQLcommand_handler, "")

		self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)

	def command_handler(self, unused_addr, args, cmdtext):
		print("{0}".format(cmdtext))
		if 'cd' in cmdtext:
			os.chdir(cmdtext.split()[1])
			res = os.getcwd()
		else:
			res=[]
			with Popen(cmdtext, stdout=PIPE, stderr=STDOUT, shell=True, universal_newlines=True) as process:
				for line in process.stdout:
					res.append(line)
		print(res)
		q.put(res)

	def SQLcommand_handler(self, unused_addr, args, qrytext):
		print("{0}".format(qrytext))
		res = ''
		if 'SELECT' in qrytext or 'select' in qrytext:
			res = db.select(qrytext)
		elif 'CREATE' in qrytext or 'create' in qrytext:
			res = db.exec(qrytext)
		elif 'INSERT' in qrytext or 'insert' in qrytext:
			res = db.exec(qrytext)
		#if len(res)==0:
		#	res='OK'
		print(res)
		q.put(res)



class client():
	def __init__(self, ip, port):
		self.client = udp_client.SimpleUDPClient(ip, port)

	def send(self):
		while 1:
			rep = q.get()
			self.client.send_message("/reply", json.dumps(rep))
			print(json.dumps(rep))
			time.sleep(1)

if __name__ == "__main__":
	# select db to connect to
	print('Opening config database')
	conf = db()
	dbname = conf.select('select lastDB from persist')[0][0]
	db = db(dbname)
	print('connecting to remote database %s' % dbname)
	#
	def worker1():
		serv = server('0.0.0.0', 8889)
		print("Serving on {}".format(serv.server.server_address))
		serv.server.serve_forever()

	def worker2():
		clint = client(otherIP, 8889)
		clint.send()

	thread_list = []
	thread1 = threading.Thread(target=worker1)
	thread_list.append(thread1)
	thread1.start()
	thread2 = threading.Thread(target=worker2)
	thread_list.append(thread2)
	thread2.start()

while 1:
	time.sleep(.5)	# uses less CPU than pass
