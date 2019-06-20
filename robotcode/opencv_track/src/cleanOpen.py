# pythonprogramminglanguage.com
import cv2
import numpy as np
import sys
from threading import Thread

class WebcamVideoStream:
    def __init__(self, src=0):
        #init camera and read first frame
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame


    def stop(self):
        self.stopped = True
        




def startCapture(vs):

    #print ('test')
    #cap = cv2.VideoCapture(0)
    #print ('success')

    while True:
        #print ('reading')
        #_, frame = cap.read()
        frame = vs.read()
        #print ('done')
        #frame = cv2.flip(frame, +1);
        #blur = cv2.GaussianBlur(frame, (15,15), 0)
        #blur = cv2.bilateralFilter(frame,9,75,75)
        #hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        #print (clock.table)


        #lower_red = np.array([clock.table['low h'],clock.table['low s'],clock.table['low v']])
        #upper_red = np.array([clock.table['high h'],clock.table['high s'],clock.table['high v']])

        #print (lower_red, upper_red)

        #high_hue = clock.table['high h']
        #low_hue = clock.table['low h']
           
        #mask = cv2.inRange(hsv, lower_red, upper_red)
        #mask = cv2.erode(mask, None, iterations=5)
        #mask = cv2.dilate(mask, None, iterations=2)
        #res = cv2.bitwise_and(frame, frame, mask = mask)
        
        #kernel = np.ones((15,15), np.float32)/255
        #smoothed = cv2.filter2D(res, -1, kernel)
        
        #median = cv2.medianBlur(res,15)
        
        
        # find contours in the mask and initialize the current
	    # (x, y) center of the ball
        #cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = cnts[1]
        # imutils.grab_contours(cnts)
        #center = None
        # only proceed if at least one contour was found
            
        #if len(cnts) > 0:
                
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            #c = max(cnts, key=cv2.contourArea)
            #((x, y), radius) = cv2.minEnclosingCircle(c)
            #M = cv2.moments(c)
            #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            #if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                #cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                #cv2.circle(frame, center, 5, (0, 0, 255), -1)

       





        #cv2.setMouseCallback("frame",on_mouse, 0);
        #s=hsv[y_co,x_co]
        #print "H:",s[0],"      S:",s[1],"       V:",s[2]
        #cv2.drawContours(frame, cnts, -1, (0,255,0), 3)





        cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        #cv2.imshow('res', res)
        #cv2.imshow('smoothed', smoothed)
        #cv2.imshow('blur', blur)
        #cv2.imshow('median', median)
        #cv2.imshow('threshold', threshold)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    #cv2.destroyAllWindows()
    vs.stop()
    
    #cap.release()
    #sys.exit(app.exec_())
    

if __name__ == '__main__':
    vs = WebcamVideoStream(src=0).start()
    startCapture(vs)  
    #clock.show()
    #vs.stream.release()
    cv2.destroyAllWindows()
    #sys.exit(app.exec_())
