"""
Initializes the main window from the Carla Experiment GUI.

Creates the Starting Window that enables users to choose between
designed a freeway experiment and an intersection experiment.
"""

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QPushButton, QWidget, QSpacerItem, QPushButton, QLabel
from PyQt5.QtGui import QFont
import freeway_window as Fway
import main_use as Inter_main

# Initialize the QApplication and capture details about the screen
app = QtWidgets.QApplication(sys.argv)
screen = app.primaryScreen()
width = screen.size().width()
height = screen.size().height()


class Start_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, width, height)
        self.setWindowTitle("UMTRI Carla Experiment Designer")
        self.initUI()

    def go_to_freeway(self):
        """
        Swap from the Starting Window to the Freeway Experiments window.
        """
        self.new = Fway.Freeway_Window(self)
        self.close()
        self.new.show()

    def go_to_intersection(self):
        """
        Swap from the Starting Window to the Intersection Experiments window.
        """
        self.new = Inter_main.Main()
        self.close()
        self.new.show()

    def initUI(self):
        """
        Initialize the UI Components on the Starting Window.

        Creates the layout, freeway button, intersection button, title label,
        and version label. Adds these elements to the window's grid layout.
        """
        self.main_widget = QWidget()
        self.grid = QGridLayout()
        self.main_widget.setLayout(self.grid)
        self.setCentralWidget(self.main_widget)

        # freeway button
        self.fway_button = QPushButton()
        self.fway_button.setText("Freeway Experiments")
        self.fway_button.setFont(QFont("Arial", 16))
        self.fway_button.setMaximumWidth(int(width/6))
        self.fway_button.setMaximumHeight(int(height/10))
        self.fway_button.clicked.connect(self.go_to_freeway)
        self.fway_button.setStyleSheet(
            "QPushButton::hover {background-color : lightblue;}"
            )

        # intersection button
        self.inter_button = QPushButton()
        self.inter_button.setText("Intersection Experiments")
        self.inter_button.setFont(QFont("Arial", 15))
        self.inter_button.setMaximumWidth(int(width/6))
        self.inter_button.setMaximumHeight(int(height/10))
        self.inter_button.clicked.connect(self.go_to_intersection)
        self.inter_button.setStyleSheet(
            "QPushButton::hover {background-color : lightblue;}"
            )

        # version text
        self.version_text = QLabel()
        self.version_text.setText(
            "University of Michigan - UMTRI - Version 1.00"
            )
        self.version_text.setFont(QFont("Arial", 18))
        self.version_text.setAlignment(QtCore.Qt.AlignCenter)
        self.version_text.setMinimumHeight(int(height/6))

        # title text
        self.title_text = QLabel()
        self.title_text.setText("Carla Simulator: User Interface")
        self.title_text.setFont(QFont("Arial", 30))
        self.title_text.setAlignment(QtCore.Qt.AlignCenter)
        self.title_text.setMinimumHeight(int(height/2))

        # spacer
        self.spacer = QSpacerItem(40, int(height/4),
                                  QtWidgets.QSizePolicy.Maximum,
                                  QtWidgets.QSizePolicy.Maximum)

        # grid
        self.grid.addWidget(self.title_text, 0, 0, 3, 2)
        self.grid.addWidget(self.fway_button, 2, 0, 1, 1)
        self.grid.addWidget(self.inter_button, 2, 1, 1, 1)
        self.grid.addWidget(self.version_text, 1, 0, 1, 2)
        self.grid.addItem(self.spacer, 3, 0, 1, 2)


def main():
    app = QApplication(sys.argv)
    win = Start_Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
