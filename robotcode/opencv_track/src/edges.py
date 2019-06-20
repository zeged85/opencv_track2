# pythonprogramminglanguage.com
import cv2
import numpy as np
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)
from collections import deque
POINTS_BUFFER = 10
x_co = 0
y_co = 0



class Window(QWidget):
    table = {}
    
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.createExampleGroup('low h'), 0, 0)
        grid.addWidget(self.createExampleGroup('low s'), 0, 1)
        grid.addWidget(self.createExampleGroup('low v'), 0, 2)
        grid.addWidget(self.createExampleGroup('high h'), 1, 0)
        grid.addWidget(self.createExampleGroup('high s'), 1, 1)
        grid.addWidget(self.createExampleGroup('high v'), 1, 2)
        grid.addWidget(self.createExampleGroup('threshold'), 2, 0)

    
        self.setLayout(grid)
        self.setWindowTitle("PyQt5 Sliders")
        self.resize(400, 300)

    def createExampleGroup(self, name):
        groupBox = QGroupBox(name)

        radio1 = QRadioButton("&Radio horizontal slider")

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(10)
        slider.setSingleStep(1)
        slider.setMinimum(0)
        slider.setMaximum(255)
        slider.valueChanged.connect(lambda cv, x=name : self.value_changed(cv, x))

        self.table[name]=0

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(slider)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def value_changed(self, value, name):  # Inside the class
    # Do the heavy task
        print (value, name)
        #for x in sliders:
        #    print (x.value())
 
        self.table[name]=value
        #print (self.table)
        sliders = list(clock.table.values())
        print (clock.table['low h'],clock.table['low s'],clock.table['low v'],clock.table['high h'],clock.table['high s'],clock.table['high v'])


def startCapture(clock):
    pts = deque(maxlen=POINTS_BUFFER)
    
    print ('test')
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        frame = cv2.flip(frame, +1);
        sliders = list(clock.table.values())
        #print (sliders)
        #t = sliders[6]
        #_, threshold = cv2.threshold(frame, t, 255, cv2.THRESH_BINARY)
        #blur = cv2.GaussianBlur(frame, (15,15), 0)
        #blur = cv2.bilateralFilter(frame,9,75,75)
        blur = frame
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        #print (clock.table)


        lower_red = np.array([clock.table['low h'],clock.table['low s'],clock.table['low v']])
        upper_red = np.array([clock.table['high h'],clock.table['high s'],clock.table['high v']])

        #print (lower_red, upper_red)

        high_hue = clock.table['high h']
        low_hue = clock.table['low h']
        
        if low_hue > high_hue:
            lower_red = np.array([0,clock.table['low s'],clock.table['low v']])
            upper_red = np.array([clock.table['high h'],clock.table['high s'],clock.table['high v']])            
            mask1 = cv2.inRange(hsv, lower_red, upper_red)
            lower_red = np.array([clock.table['low h'],clock.table['low s'],clock.table['low v']])
            upper_red = np.array([179,clock.table['high s'],clock.table['high v']])            
            mask2 = cv2.inRange(hsv, lower_red, upper_red)
            mask = cv2.bitwise_or(mask1,mask2)
        else:
            
            
            mask = cv2.inRange(hsv, lower_red, upper_red)
        mask = cv2.erode(mask, None, iterations=5)
        mask = cv2.dilate(mask, None, iterations=2)
        res = cv2.bitwise_and(frame, frame, mask = mask)
        
        #kernel = np.ones((15,15), np.float32)/255
        #smoothed = cv2.filter2D(res, -1, kernel)
        
        #median = cv2.medianBlur(res,15)
        
        
        # find contours in the mask and initialize the current
	# (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[1]
        # imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
            
        if len(cnts) > 0:
                
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the points queue
        pts.appendleft(center)


        # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(POINTS_BUFFER / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)








        #cv2.setMouseCallback("frame",on_mouse, 0);
        s=hsv[y_co,x_co]
        #print "H:",s[0],"      S:",s[1],"       V:",s[2]
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = 1
        fontcolor = (255, 255, 255)
        #cv2.putText(im, str(Id), (x,y+h), fontface, fontscale, fontcolor) 
        cv2.putText(frame,str(s[0])+","+str(s[1])+","+str(s[2]), (x_co,y_co),fontface, fontscale, fontcolor)
        cv2.drawContours(frame, cnts, -1, (0,255,0), 3)





        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        #cv2.imshow('smoothed', smoothed)
        #cv2.imshow('blur', blur)
        #cv2.imshow('median', median)
        #cv2.imshow('threshold', threshold)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    #sys.exit(app.exec_())
    
def on_mouse(event,x,y,flag,param):
    print (event)
    global x_co
    global y_co
    if(event==1):
        x_co=x
        y_co=y


if __name__ == '__main__':
    app = QApplication(sys.argv)
  
    clock = Window()
    clock.show()
    startCapture(clock)


    
    #clock.show()

    sys.exit(app.exec_())
