#!/usr/bin/env python

import roslib
import sys
import rospy
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')# before you import cv2
#sys.path.remove('/usr/lib/python2.7/dist-packages')
#print sys.path
#import cv2
import cv2
print cv2.__version__
#sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')# before you import cv2
#sys.path.append('/usr/lib/python2.7/dist-packages')
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image, LaserScan
import math

last_value = 0.0
laser_values = np.full(360, np.inf)
last_value_wall = 0.0


class LineFollower(object):
	def __init__(self):

		self.bridge_object = CvBridge()
		self.image = rospy.Subscriber("/tb3_0/camera/rgb/image_raw",Image,self.camera_callback)

	def camera_callback(self,data):

		try:
			# We select bgr8 because its the OpenCV encoding by default
			cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")

			#crop
			height, width, channels = cv_image.shape
			descentre = -140
			rows_to_watch = 200
			crop_image = cv_image[(height)/2+descentre:(height)/2+(descentre+rows_to_watch)][1:width]

			#hsv
			hsv = cv2.cvtColor(crop_image,cv2.COLOR_BGR2HSV)

			#mask
			lower_red = np.array([0,100,100])
			upper_red = np.array([0,255,255])

			mask = cv2.inRange(hsv, lower_red, upper_red)

			#calc centroid using image moments
			m = cv2.moments(mask,False)
			
			target_found = False
			
			try:
				cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
				target_found = True
			except ZeroDivisionError:
				cx, cy = width/2, height/2

			#draw centroids
			#cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
			res = cv2.bitwise_and(crop_image, crop_image, mask=mask)
			_, contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
			centers = []
			for i in range(len(contours)):
				moments = cv2.moments(contours[i])
				try:
					centers.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
					cv2.circle(res, centers[-1], 10, (0,255,0), -1)
				except ZeroDivisionError:
					pass



			cv2.circle(res, (int(cx), int(cy)), 10, (255,0,0), -1)


			#choose first circle
			if target_found and len(centers)>0:
				cx, cy = centers[0]


			global last_value
			set_point = width/2
			current_value = cx
			kp = -0.001
			kd = 0.01
		


			keep_distance = 0.3
			vel = 0.0
			ang = 0.0
			d = (cx - width/2)*kd
			p = (cx - width/2 - last_value)*kp


			ang = p + d
			#ang *= -1

			spectrum = 20
			
			mid = np.amin(np.concatenate((laser_values[-spectrum:], laser_values[:spectrum]), axis=0) )
			right = np.amin(laser_values[-2*spectrum:-spectrum])
			left = np.amin(laser_values[spectrum:spectrum*2])

			#print 'left', left, 'mid', mid, 'right', right, ' ang', ang

			if target_found:
	
				if mid<1.5:
					#drive(mid - keep_distance ,ang)
					vel = mid - keep_distance
				else:
					#drive(1,ang)
					vel = 1
			else:
				#drive(0,0)
				vel = 0
				ang = 0


				
			last_value = cx
			vel=0
			drive(vel,-ang)

			#print 'height', height, ' width', width, ' cx:',cx


		except CvBridgeError as e:
			print(e)

		#print(cv2)
		cv2.imshow("Image window", cv_image)
		#cv2.imshow("Cropped", crop_image)
		#cv2.imshow("HSV", hsv)
		cv2.imshow("Masked", res)
		cv2.waitKey(1)

pub_ = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=50)
def main():
	#wheel_radius = rospy.get_param('/tb3_1/mobile_base_controller/wheel_radius')
	#wheel_separation = rospy.get_param('/tb3_1/mobile_base_controller/wheel_separation')

	#/tb3_1/mobile_base_controller/wheel_separation
	#pub_ = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=50)
	rospy.init_node('line_following_node', anonymous=True)
	rospy.Subscriber("/tb3_0/scan", LaserScan, scan_cb, queue_size=1)
	line_follower_object = LineFollower()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()


def scan_cb(msg):
	#print len(msg.ranges)
	global laser_values
	laser_values = np.array( msg.ranges )
	#print '0',laser_values[0]
	#print '90',laser_values[90]
	#print '180',laser_values[180]
	#print '270',laser_values[270]

	#180/5 = 36
	silces = 5
	size = 36
	regions = {
		'right':  min(min(msg.ranges[269:305]), 3),
		'fright': min(min(msg.ranges[306:341]), 3),
		'front':  min(min(np.concatenate((msg.ranges[342:],msg.ranges[:17]),axis=0)), 3),
		'fleft':  min(min(msg.ranges[18:53]), 3),
		'left':   min(min(msg.ranges[54:89]), 3),
		}
	#print regions
	take_action(regions)
	#pid(regions)


def pid(wall, regions):
	global last_value_wall
	set_point = 0.30
	#keep_distance = 0.1
	if wall == 'left':
		current_value = min(min(laser_values[10:75]), 3)
	else:
		current_value = min(min(laser_values[314:349]), 3)

	print current_value
	kp = -3.0
	kd = 12.5
	
	vel = 0.6
	left = vel / 2
	right = vel / 2
	ang = 0.0
	d = (set_point - current_value)*kd
	p = (set_point - current_value - last_value_wall)*kp
	ang = p + d
	k=0.1
	print 'ang', ang
	#vel = 0.3 - abs(ang*k/kd)
	if regions['front'] < 1.0:
		ang+=regions['front']
	left -= ang*k
	right += ang*k
	print 'left', left, 'right', right
	#last_value_wall = current_value

	if wall=='right':
		drive_left_right(right,left)
	else:
		drive_left_right(left,right)
	
def drive_left_right(left,right):
	wheelSeparation = 0.287
	#wheelDiameter = 0.066
	vel = (left + right) /2
	rot = (left - right) / wheelSeparation
	drive(vel,rot)
	

def drive(x,z):

	msg = Twist()
	msg.linear.x = x
	msg.linear.y = 0
	msg.angular.z = z
	speed = 0.4 
	#rospy.loginfo("checking for cmd" + str(msg.linear))
	#print 'x:', msg.linear.x
	#print 'z:', msg.angular.z
	pub_.publish(msg)


def take_action(regions):
	msg = Twist()
	linear_x = 0
	angular_z = 0

	state_description = ''
	front_limit = 0.9
	side_limit = 1.0
    
	if regions['front'] > front_limit and regions['fleft'] > side_limit and regions['fright'] > side_limit:
		state_description = 'case 1 - nothing'
		#linear_x = 0.6
		angular_z = 0
	elif regions['front'] < front_limit and regions['fleft'] > side_limit and regions['fright'] > side_limit:
		state_description = 'case 2 - front'
		linear_x = 0
		angular_z = 0.3
	elif regions['front'] > front_limit and regions['fleft'] > side_limit and regions['fright'] < side_limit:
		state_description = 'case 3 - fright'
		linear_x = 0
		angular_z = 0.3
		pid('right',regions)
	elif regions['front'] > front_limit and regions['fleft'] < side_limit and regions['fright'] > side_limit:
		state_description = 'case 4 - fleft'
		linear_x = 0
		angular_z = -0.3
		pid('left',regions)
	elif regions['front'] < front_limit and regions['fleft'] > side_limit and regions['fright'] < side_limit:
		state_description = 'case 5 - front and fright'
		linear_x = 0
		angular_z = 0.3
	elif regions['front'] < front_limit and regions['fleft'] < side_limit and regions['fright'] > side_limit:
		state_description = 'case 6 - front and fleft'
		linear_x = 0
		angular_z = -0.3
	elif regions['front'] < front_limit and regions['fleft'] < side_limit and regions['fright'] < side_limit:
		state_description = 'case 7 - front and fleft and fright'
		if regions['front'] < 0.5:
			linear_x = -0.1
			angular_z = -0.3
			state_description+=' - To close!'
		else:
			linear_x = 0.1
			angular_z = 0.3
	elif regions['front'] > front_limit and regions['fleft'] < side_limit and regions['fright'] < side_limit:
		state_description = 'case 8 - fleft and fright'
		linear_x = 0.3
		angular_z = 0
	else:
		state_description = 'unknown case'
		rospy.loginfo(regions)

	rospy.loginfo(state_description)
	msg.linear.x = linear_x
	msg.angular.z = angular_z
	#pub_.publish(msg)


if __name__ == '__main__':
	main()
