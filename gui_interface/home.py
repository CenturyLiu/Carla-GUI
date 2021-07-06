from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
import sys
import freeway_window as Fway
import intersection_window as Inter

import time
import glob
import os
import sys
sys.path.append("..")


#get user screen size
app = QtWidgets.QApplication(sys.argv)
screen = app.primaryScreen()
width = screen.size().width()
height = screen.size().height()


class Start_Window(QMainWindow):
    def __init__(self):
        super(Start_Window, self).__init__()
        self.setGeometry(0,0,width,height)
        self.setWindowTitle("Start")
        self.initUI()

    def initUI(self):
        self.main_widget = QWidget()
        self.grid = QGridLayout()
        self.main_widget.setLayout(self.grid)
        self.setCentralWidget(self.main_widget)
        

        #freeway button
        self.fway_button = QPushButton()
        self.fway_button.setText("Freeway")
        self.fway_button.setFont(QFont("Arial", 18))
        self.fway_button.setMaximumWidth(int(width/7))
        self.fway_button.setMaximumHeight(int(height/10))
        self.fway_button.clicked.connect(self.go_to_freeway)
        

        #intersection button
        self.inter_button = QPushButton()
        self.inter_button.setText("Intersection")
        self.inter_button.setFont(QFont("Arial", 18))
        self.inter_button.setMaximumWidth(int(width/7))
        self.inter_button.setMaximumHeight(int(height/10))
        self.inter_button.clicked.connect(self.go_to_intersection)
        

        #version text
        self.version_text = QLabel()
        self.version_text.setText("University of Michigan - UMTRI - Version 1.00")
        self.version_text.setFont(QFont("Arial", 18))
        self.version_text.setAlignment(QtCore.Qt.AlignCenter)
        self.version_text.setMinimumHeight(int(height/6))


        #title text
        self.title_text = QLabel()
        self.title_text.setText("Carla Simulator: User Interface")
        self.title_text.setFont(QFont("Arial", 30))
        self.title_text.setAlignment(QtCore.Qt.AlignCenter)
        self.title_text.setMinimumHeight(int(height/2))

        #spacer
        self.spacer = QSpacerItem(40,int(height/4),QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum)

        """
        #loading box
        self.loading = QDialog(self)
        self.loading.move(width/2,height/2)
        self.loading.setMinimumWidth(width/6)
        self.loading.setMinimumHeight(height/6)
        self.loading.setMaximumWidth(width/6)
        self.loading.setMaximumHeight(height/6)
        self.loading.hide()

        self.loading_label = QLabel(self.loading)
        self.loading_label.setText("Loading...")
        """
        

        #grid
        self.grid.addWidget(self.title_text,0,0,3,2)
        self.grid.addWidget(self.fway_button,2,0,1,1)
        self.grid.addWidget(self.inter_button,2,1,1,1)
        self.grid.addWidget(self.version_text,1,0,1,2)
        self.grid.addItem(self.spacer,3,0,1,2)
        

    def go_to_freeway(self):
        """
        connected: self.freeway_button
        function: destroys self and goes to freeway gui
        """
        self.new = Fway.Freeway_Window(self)
        self.close()
        self.new.show()

    def go_to_intersection(self):
        """
        connected: self.intersection_button
        function: destroys self and goes to urban gui
        """
        self.new = Inter.Intersection_Window(self)
        self.close()
        self.new.show()

def main():
    app = QApplication(sys.argv)
    win = Start_Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
