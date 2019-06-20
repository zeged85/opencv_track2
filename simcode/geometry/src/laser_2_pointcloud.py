#! /usr/bin/env python

import sensor_msgs.point_cloud2 as pc2
import rospy
from roslib import message
from sensor_msgs.msg import PointCloud2, LaserScan
import laser_geometry.laser_geometry as lg
import math
from collections import namedtuple
from Tkinter import *
import random
from geometry_msgs.msg import Twist 

COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

canvas_width = 1500
canvas_height = 1500
factor = 200

rospy.init_node("laserscan_to_pointcloud")

lp = lg.LaserProjection()

cloud_points = list();
old_points = list();


def send_position(cluster):
	msg = Twist()
	msg.linear.x = 0
	#2 - math.sqrt(cluster[0][0]*cluster[0][0] + cluster[0][1]*cluster[0][1])
	msg.linear.y = 0
	msg.angular.z = cluster[0][0]-cluster[-1][0]
	speed = 0.4 
	#rospy.loginfo("checking for cmd" + str(msg.linear))
	print 'x:', msg.linear.x
	print 'y:', msg.angular.z
	pub_.publish(msg)


def get_Distance(p1, p2):
	distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
	return distance

def get_Coeff(p1,p2):
	a = p1[0]-p2[0]
	b = p2[1]-p1[1]
	c = p1[1]*p2[0] - p2[1]*p1[0]
	return a,b,c
	

def cluster_analysis(points):
	clusters = list()
	cluster = list()
	new_clusters = list()
	for point in points:
		if len(cluster)==0:
			cluster.append(point)
		else:
			dist = get_Distance(cluster[-1],point)
			if dist < 0.15:
				cluster.append(point)
			else:
				clusters.append(list(cluster))
				cluster = list()
			

	print 'found ', len(clusters), ' clusters'
	count = 0
	for cluster in clusters:
		count+=1
		width = get_Distance(cluster[0],cluster[-1])
		girth = 0.0
		a,b,c = get_Coeff(cluster[0],cluster[-1])
		x = 1
		max_distance = 0.0
		while x<len(cluster):
			girth+=get_Distance(cluster[x-1],cluster[x])
			distance = math.fabs(a * cluster[x][1] + b * cluster[x][0] + c ) / math.sqrt(a*a + b*b)
			if distance > max_distance:
				max_distance = distance
			x+=1

	
		depth = max_distance
		print 'cluster #', count, ' width:', width, ' girth:', girth, ' depth:', max_distance, ' distance:', math.sqrt(cluster[0][0]*cluster[0][0]+cluster[0][1]*cluster[0][1])
		if width > 0.108 and width < 0.557 and depth > 0.008 and depth < 0.364 and girth < 1.07 and girth > 0.15:
			print 'pass'
			#and len(cluster)>5 and len(cluster) < 20
			new_clusters.append (list(cluster))

	if len(new_clusters) >= 1:
		send_position(new_clusters[0])
	else:
		send_position([[0,0]])

	return new_clusters, clusters


def get_rand_color():
	de=("%02x"%random.randint(0,255))
	re=("%02x"%random.randint(0,255))
	we=("%02x"%random.randint(0,255))
	ge="#"
	color=ge+de+re+we
	return color

def paint():

	clusters_match, clusters_nomatch = cluster_analysis(cloud_points)
	
	python_green = "#476042"

	#print 'in paint'
	global old_points
	for point in old_points:
		canvas.delete(point)
	old_points = list()



	for cluster in clusters_nomatch:
		color = COLORS[10]
		#i+=5
		for point in cluster:
			if not math.isnan(point[2]):
				#print 'seq:', count, ' point:', point
				
				y1, x1 = -(point[0] - 0.02), -(point[1] - 0.02)
				y2, x2 = -(point[0] + 0.02), -(point[1] + 0.02)
				pixel = canvas.create_oval(canvas_width/2 +x1 * factor,canvas_height/2 + y1 * factor,canvas_width/2 + x2 * factor, canvas_height/2 + y2 * factor, fill=color)
				old_points.append(pixel);



	i = 30
	for cluster in clusters_match:
		color = COLORS[i]
		i+=5
		for point in cluster:
			if not math.isnan(point[2]):
				#print 'seq:', count, ' point:', point
				
				y1, x1 = -(point[0] - 0.02), -(point[1] - 0.02)
				y2, x2 = -(point[0] + 0.02), -(point[1] + 0.02)
				pixel = canvas.create_oval(canvas_width/2 +x1 * factor,canvas_height/2 + y1 * factor,canvas_width/2 + x2 * factor, canvas_height/2 + y2 * factor, fill=color)
				old_points.append(pixel);

	

	master.after(20, paint)



#pc_pub = rospy.Publisher("converted_pc", PointCloud2, queue_size=1)

def scan_cb(msg):
	# convert the message of type LaserScan to a PointCloud2
	pc2_msg = lp.projectLaser(msg)

	# now we can do something with the PointCloud2 for example:
	# publish it
	#pc_pub.publish(pc2_msg)
 
	# convert it to a generator of the individual points
	point_generator = pc2.read_points(pc2_msg)
    
	global cloud_points
	cloud_points = list(pc2.read_points(pc2_msg, skip_nans=True, field_names = ("x", "y", "z")))

	# we can access a generator in a loop
	sum = 0.0
	num = 0
	count = 0;
	for point in cloud_points:
		if not math.isnan(point[2]):
			#print 'seq:', count, ' point:', point
			count+=1;
			sum += point[2]
			num += 1
		else:
			#print 'seq:', count, ' point:', point	
			pass
		# we can calculate the average z value for example
	
	#print(str(sum/num))

    # or a list of the individual points which is less efficient
    #point_list = pc2.read_points_list(pc2_msg)

    #point_list = pc2.read_points(pc2_msg, field_names=None, skip_nans=False)

    # we can access the point list with an index, each element is a namedtuple
    # we can access the elements by name, the generator does not yield namedtuples!
    # if we convert it to a list and back this possibility is lost

    #print point_list[0]
    #print(point_list[len(point_list)/2].x)




master = Tk()
master.title("Points")
canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack(expand=YES, fill=BOTH)

canvas.create_oval(canvas_width/2-10,canvas_height/2 -10,canvas_width/2 + 10, canvas_height/2 + 10)


pub_ = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=50)
rospy.Subscriber("/tb3_0/scan", LaserScan, scan_cb, queue_size=1)

paint();

#rospy.spin()
master.mainloop()
