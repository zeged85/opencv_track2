#! /usr/bin/env python
 
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist 

seq = 0;

left = 0;
mid=0;
right=0;
 
def callback(msg):
	global seq
	global left
	global mid
	global right
	print 'seq:', seq, ' array size: ',len(msg.ranges)
	# values at 0 degree
	print msg.ranges[719]
	left = msg.ranges[719]

	

	# values at 90 degree
	print msg.ranges[360]
	mid = msg.ranges[360]
	# values at 180 degree
	print msg.ranges[0]
	right = msg.ranges[0]	
	seq+=1

	#setSpeed(5,0)
	








 
rospy.init_node('scan_values')
sub = rospy.Subscriber('/robot2/scan', LaserScan, callback)
pub_ = rospy.Publisher('/robot2/mobile_base_controller/cmd_vel', Twist, queue_size=50)






def setSpeed(liner_x,angular_z ):

	#rospy.loginfo("Classifiers output: %s in unknown" % data.data)
	#rospy.sleep(2.)
	msg = Twist()
	msg.linear.x = liner_x
	msg.linear.y = 0
	msg.angular.z = -angular_z
	#speed = 0.4 
	#rospy.loginfo("checking for cmd" + str(msg.linear))
	rospy.sleep(0.2)
	pub_.publish(msg)


#find local max
max_found = False
max = 0.0
min = 10.0
while (not max_found):

	setSpeed(0,0)
	print 'wait pls'
	rospy.sleep(2)


	while (mid>10.0):
		#print 'max: ',max
		if (mid < min):
			
			min = mid	
	
		setSpeed(0,5)


	#max found
	#go back
	setSpeed(0,0)
	rospy.sleep(2)
	max = mid
	while(mid > min):
		#print 'min: ',min		
		if (mid > max):

			max = mid
		
	
		setSpeed(0,-1)
	

	max_found = True;



	
setSpeed(0,2)
rospy.sleep(3)


rospy.spin()
