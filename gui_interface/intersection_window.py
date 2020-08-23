from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
import sys

import home as primary

class Intersection_Window(QMainWindow):
    def __init__(self,parent=None):
        super(Intersection_Window, self).__init__(parent)
        self.setGeometry(0,0,primary.width,primary.height)
        self.setWindowTitle("Intersection")
        self.initUI()


    def initUI(self):#set min sizes!!! helps rescaling
        self.main_widget = QWidget()
        self.grid = QGridLayout()
        self.main_widget.setLayout(self.grid)
        self.setCentralWidget(self.main_widget)


        #back button
        self.back_button = QPushButton()
        self.back_button.setText("Back to Start")
        self.back_button.clicked.connect(self.back_to_start)

        #text
        self.num_sections_box = QLineEdit()


        #grid
        self.grid.addWidget(self.back_button)
        self.grid.addWidget(self.num_sections_box)
    

    def back_to_start(self):
        self.new = primary.Start_Window()
        self.close()
        self.new.show()