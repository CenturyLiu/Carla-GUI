from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import edit_section
import freeway_window
import home as primary
import carla_vehicle_list



class Back_Home_Pop_Up(QDialog):
    """
    dialog box that will pop up when attempting to go back to home.py to warn users of settings loss
    """
    def __init__(self,parent=None):
        super(Back_Home_Pop_Up, self).__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Back")
        self.initUI()

    def initUI(self):
        self.grid = QVBoxLayout()
        self.setLayout(self.grid)
        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setAlignment(QtCore.Qt.AlignCenter)

        #set size values
        self.setMinimumHeight(primary.height/3)
        self.setMinimumWidth(primary.width/4)
        self.setMaximumHeight(primary.height/3)
        self.setMaximumWidth(primary.width/4)



        #text
        self.back_text = QLabel()
        self.back_text.setText("Going back to start will delete all current settings.")

        #spacer
        self.spacer = QLabel()
        self.spacer.setMinimumHeight(self.height()/6)
        
        #back button
        self.back_button = QPushButton()
        self.back_button.setText("Go Back")
        self.back_button.setMaximumWidth(self.width()/1.4)
        self.back_button.clicked.connect(self.parent_window.back_to_start)



        #GRID SETTINGS
        self.grid.addWidget(self.back_text)
        self.grid.addWidget(self.spacer)
        self.grid.addWidget(self.back_button)
        
        


        











def main():
    primary.main()


if __name__ == "__main__":
    main()