# pythonprogramminglanguage.com
import cv2
import numpy as np
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider)




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


def startCapture(clock):
    
    print ('test')
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #print (clock.table)
        sliders = list(clock.table.values())
        print (sliders)

        lower_red = np.array([sliders[0],sliders[1],sliders[2]])
        upper_red = np.array([sliders[3],sliders[4],sliders[5]])

        #print (lower_red, upper_red)

        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(frame, frame, mask = mask)
        
        kernel = np.ones((15,15), np.float32)/255
        smoothed = cv2.filter2D(res, -1, kernel)
        blur = cv2.GaussianBlur(res, (15,15), 0)
        median = cv2.medianBlur(res,15)
        _, threshold = cv2.threshold(res, 12, 255, cv2.THRESH_BINARY)





        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        #cv2.imshow('smoothed', smoothed)
        #cv2.imshow('blur', blur)
        #cv2.imshow('median', median)
        cv2.imshow('threshold', threshold)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    #sys.exit(app.exec_())
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
  
    clock = Window()
    clock.show()
    startCapture(clock)


    
    #clock.show()

    sys.exit(app.exec_())
