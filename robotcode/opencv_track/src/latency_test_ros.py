"""
Run this script then
point the camera to look at the window,
watch the color flips between black and white.
Slightly increase "THRESHOLD" value if it doesn't flip.
"""

import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rospy
import time

# Initialize USB webcam feed
CAM_INDEX = 0
# Adjust this value if it doesn't flip. 0~255
THRESHOLD = 100
# Set up camera constants
IM_WIDTH = 1280
IM_HEIGHT = 720
# IM_WIDTH = 640
# IM_HEIGHT = 480

### USB webcam ###
#camera = cv2.VideoCapture(CAM_INDEX)
#if ((camera == None) or (not camera.isOpened())):
#    print('\n\n')
#    print('Error - could not open video device.')
#    print('\n\n')
#    exit(0)
#camera.set(cv2.CAP_PROP_FRAME_WIDTH, IM_WIDTH)
#camera.set(cv2.CAP_PROP_FRAME_HEIGHT, IM_HEIGHT)
# save the actual dimensions
#actual_video_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
#actual_video_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
#print('actual video resolution:{:.0f}x{:.0f}'.format(actual_video_width, actual_video_height))

bridge_object = CvBridge()
newFrame = False

cv_image = np.empty((0))

def camera_callback(data):
	global newFrame
	
	#self.recieved_image = True
	#try:
	# We select bgr8 because its the OpenCV encoding by default
	global cv_image	
	cv_image = bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
		#crop
	newFrame = True
	height, width, channels = cv_image.shape
	#print 'Proccessing frame | Delay:%6.3f' % (rospy.Time.now() - data.header.stamp).to_sec()

rospy.init_node('latency_test_node', anonymous=True)

image = rospy.Subscriber("/usb_cam/image_raw",Image,camera_callback)

rate = rospy.Rate(10)

prev_tick = cv2.getTickCount()
frame_number, prev_change_frame = 0, 0
is_dark = True

while not rospy.is_shutdown():
	if newFrame == False:
		#print 'false'
		#rospy.spin()
		continue
	newFrame = False
	#print 'frame'
	frame_number += 1

	img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

	is_now_dark = np.average(img) < THRESHOLD


	if is_dark != is_now_dark:
		is_dark = is_now_dark
		new = cv2.getTickCount()
		print("{:.3f} sec, {:.3f} frames".format((new - prev_tick) / cv2.getTickFrequency(),frame_number - prev_change_frame))
		prev_tick = new
		prev_change_frame = frame_number
		fill_color = 255 if is_dark else 0
		show = np.full(img.shape, fill_color, dtype=img.dtype)


		cv2.imshow('frame', show)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break



camera.release()

cv2.destroyAllWindows()	


'''
while True:
    frame_number += 1

    _, frame = camera.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    is_now_dark = np.average(img) < THRESHOLD

    if is_dark != is_now_dark:
        is_dark = is_now_dark
        new = cv2.getTickCount()

        print("{:.3f} sec, {:.3f} frames".format(
            (new - prev_tick) / cv2.getTickFrequency(),
            frame_number - prev_change_frame
        ))
        prev_tick = new

        prev_change_frame = frame_number

        fill_color = 255 if is_dark else 0
        show = np.full(img.shape, fill_color, dtype=img.dtype)

        cv2.imshow('frame', show)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
'''
