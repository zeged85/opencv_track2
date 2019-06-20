#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class MoveRobot(object):
	def __init__(self):
		self.cmd_vel_pub = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=50)
		self.cmd_vel_sub = rospy.Subscriber('/tb3_0/cmd_vel', Twist, self.cmdvel_callback)
		self.last_cmdvel_command = Twist()
		self._cmdvel_pub_rate = rospy.Rate(10)
		self.shutdown_detected = False

	def cmdvel_callback(self,msg):
		self.last_cmdvel_command = msg

	def 
