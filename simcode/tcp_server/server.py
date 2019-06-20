#!/usr/bin/env python

#https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
import select, socket, sys, Queue
import datetime
import logging
import ConfigParser

import math

import subprocess
address = subprocess.check_output(['hostname', '-s', '-I'])
address = address.decode('utf-8') 
address=address[:-1]
address=address.split(' ')[0]
print 'address:', address



import rospy
from geometry_msgs.msg import Twist 


rospy.init_node('my_node_name1')

msg = Twist()

pub_ = rospy.Publisher('/tb3_1/mobile_base_controller/cmd_vel', Twist, queue_size=50)
#rospy.loginfo("Classifiers output: %s in unknown" % data.data)
rospy.sleep(2.)

#msg.linear.x = 2
#msg.linear.y = 0
#msg.angular.z = 2
#speed = 0.4 
#rospy.loginfo("checking for cmd" + str(msg.linear))
#pub_.publish(msg)






LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename='server.log',level=logging.NOTSET, format=LOG_FORMAT, stream=sys.stdout)
logger = logging.getLogger()

str = "255.255.255.255:65535"

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)-8s  %(asctime)-12s  '+ str +'  %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)



logger.info("this is an info message")
logger.debug("this is a debug message")
logger.warning("this is a warning message")
logger.error("this in an error")
logger.critical("this is critical")




#sys.exit()

Config = ConfigParser.ConfigParser()
Config.read("server.ini")
print Config.sections()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
#TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_IP = address
TCP_PORT = 5005

server.bind((TCP_IP, 0))
server.listen(5)



print 'server started. listening on ', TCP_IP, ':',server.getsockname()[1]
inputs = [server]
outputs = []
message_queues = {}
addresses = {}

while inputs:
	readable, writable, exceptional = select.select(inputs, outputs, inputs)
	for s in readable:
		if s is server:
			connection, client_address = s.accept()
			log =  'connected: {time}, {address}'.format(time=datetime.datetime.now(), address=client_address)
			print log
			logger.warning(log)
			#print 'New connection on address:', client_address
			connection.setblocking(0)
			inputs.append(connection)
			message_queues[connection] = Queue.Queue()
			message_queues[connection].put('hello new client\n')#shouldn't we wait for client request first?
			addresses[connection]=client_address;
		else:
			data = s.recv(1024)
			if data and data!='SHTD3':
				#log =  'received: {time}, {address}, {data}'.format(time=datetime.datetime.now(), address=addresses[connection], data=data)
				#print log
				#logger.warning(log)
				for con in addresses:
					message_queues[con].put(data)
					if con not in outputs:
						outputs.append(con)
				if s not in outputs:
					outputs.append(s)
				idxl = data.rfind("<")
				idxr = data.rfind(">")
				if (idxl>= 0 and idxl<idxr):
					

				
					message = data[idxl+1:idxr].split(":")
					if (message[0]=="TouchBegin" or message[0]=="TouchMove"):
						print 'x:', message[1]
						print 'y:', message[2]
						msg.linear.x = (0.5-float(message[2]))*10
						msg.angular.z = (1-0.5-float(message[1]))*20
						pub_.publish(msg)	
	
					else:
						print 'stop'
						msg.linear.x = 0
						msg.angular.z = 0
						pub_.publish(msg)



			else:
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				s.close()
				del message_queues[s]
				log =  'disconnected: {time}, {address}'.format(time=datetime.datetime.now(), address=addresses[connection])
				#print log
				logger.warning(log)
				del addresses[connection]
	for s in writable:
		try:
			next_msg = message_queues[s].get_nowait()
			#print 'got msg:', next_msg
		except Queue.Empty:
			outputs.remove(s)
		except:
			print "Unexpected error:", sys.exc_info()[0]
		else:
			s.send(next_msg)
			print 'sent msg:', next_msg
	
	for s in exceptional:
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()
		del message_queues[s]
		log =  'disconnected: {time}, {address}'.format(time=datetime.datetime.now(), address=addresses[connection])
		#print log
		logger.warning(log)
		del addresses[connection]
