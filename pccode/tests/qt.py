# pythonprogramminglanguage.com
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
        print (self.table)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())
