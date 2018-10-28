"""

OsClip: bi-directional clipboard sharing between computers (PC or Mac)
	based on pyperclip and python-osc

by:			zappfinger (Richard van Bemmelen)
version:	1.0
date:		13-10-2018

"""

from pythonosc import dispatcher
from pythonosc import osc_server, udp_client
import threading
import pyperclip
from commands import *

"""
	enter the name of the SQLite machine to connect to
"""
##########################
name = 'PCToos'
##########################
conf = db()
otherIP = conf.select('select IP from nodes where name="%s" ' % name)[0][0]

magic = 'm@gic:'

class server():
	def __init__(self, ip, port):
		self.dispatcher = dispatcher.Dispatcher()
		self.dispatcher.map("/clip", self.print_clip_handler, "")
		self.server = osc_server.ThreadingOSCUDPServer((ip, port), self.dispatcher)

	def print_clip_handler(self, unused_addr, args, cliptext):
		print("{0}".format(cliptext))
		if magic in cliptext:
			cliptext = cliptext[6:]
			pyperclip.copy(cliptext)

class client():
	def __init__(self, ip, port):
		self.oldclip = ''
		self.client = udp_client.SimpleUDPClient(ip, port)

	def send(self):		# send when clipboard has changed
		while 1:
			pasted = pyperclip.paste()
			if not (magic in pasted) and pasted!= self.oldclip:
				self.client.send_message("/clip", magic + pasted)
				self.oldclip = pasted
				print(self.oldclip)
			time.sleep(1)

if __name__ == "__main__":
	def worker1():
		serv = server('0.0.0.0', 8888)
		print("Serving on {}".format(serv.server.server_address))
		serv.server.serve_forever()

	def worker2():
		clint = client(otherIP, 8888)
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
