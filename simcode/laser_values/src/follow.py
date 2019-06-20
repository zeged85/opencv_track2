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


	left = 10
	mid = 10
	right = 10

	print 'seq:', seq, ' array size: ',len(msg.ranges)

	# values at 0 degree
	
	for x in range(719-250,719):
		if (msg.ranges[x]<left):
			left = msg.ranges[x]
	print left

	
	
	# values at 90 degree

	for x in range(360-40,360+40):
		if (msg.ranges[x]<mid):
			mid = msg.ranges[x]
	print mid


	# values at 180 degree

	for x in range(0,250):
		if (msg.ranges[x]<right):
			right = msg.ranges[x]

	print right	
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


#follow

while (True):
	linear = 0
	angular = 0
	if (left > 2 and right > 2):
		if (mid>1.5 and mid < 5):
			linear=5
		elif (mid<1 and mid > 0.5):
			linear=-5

	if (left < 5):
		angular = -5
	if (right < 5):
		angular = 5

	
	if (mid < 0.5):
		linear = -2,0

	setSpeed(linear,angular)


rospy.sleep(0.2)


rospy.spin()
