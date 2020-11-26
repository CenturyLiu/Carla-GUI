from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import edit_section
import freeway_window
import home as primary


"""
ORIGINAL DESIGN SUPPORTED VEHICLE EDITING IN ADD_VEHICLE.PY
THIS PAGE IS NOW UNUSED BUT IS BEING LEFT FOR FUTURE REFERENCE OR IMPLEMENTATION
YOU CAN DELETE THIS FILE IF YOU PLESE
"""
class Drop_Down_Window_Edit(QDialog):
    def __init__(self,lane,parent=None):
        super(Drop_Down_Window_Edit, self).__init__(parent)
        self.parent_window = parent
        self.lane = lane
        self.initUI()


    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setContentsMargins(0,0,0,0)

        self.setMinimumHeight(primary.height/3)
        self.setMinimumWidth(primary.width/8)
        self.setMaximumHeight(primary.height/3)
        self.setMaximumWidth(primary.width/8)

        """
        #close button
        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.clicked.connect(self.close)
        """

        #subject lane lists
        self.subject_labels = list()
        self.subject_delete_buttons = list()

        #left lane lists
        self.left_labels = list()
        self.left_delete_buttons = list()

        if self.lane == "subject":
            for index,car in enumerate(self.parent_window.subject_vehicle_list):
                self.car_label = QLabel()
                self.car_label.setText("Vehicle {}".format(car.text()))
                self.subject_labels.append(self.car_label)

                self.delete_button = QPushButton()
                self.delete_button.setText("Delete")
                self.delete_button.clicked.connect(self.delete_car(index,"subject"))
                self.delete_button.setStyleSheet("QPushButton::hover"
                "{"
                "background-color : lightblue;"
                "}")
                self.subject_delete_buttons.append(self.delete_button)

                self.grid.addWidget(self.car_label,         index+1,0,1,1)
                self.grid.addWidget(self.delete_button, index+1,1,1,1)
        else:
            for index,car in enumerate(self.parent_window.left_vehicle_list):
                self.car_label = QLabel()
                self.car_label.setText("Vehicle {}".format(car.text()))
                self.left_labels.append(self.car_label)

                self.delete_button = QPushButton()
                self.delete_button.setText("Delete")
                self.delete_button.clicked.connect(self.delete_car(index,"left"))
                self.delete_button.setStyleSheet("QPushButton::hover"
                "{"
                "background-color : lightblue;"
                "}")
                self.left_delete_buttons.append(self.delete_button)


                self.grid.addWidget(self.car_label,         index+1,0,1,1)
                self.grid.addWidget(self.delete_button, index+1,1,1,1)

        




    def close(self):
        self.hide()
        self.parent_window.hide()
        self.parent_window.show()
        self.parent_window.subject_lane_add_vehicle.setEnabled(True)
        self.parent_window.subject_lane_edit_lane.setEnabled(True)
        self.parent_window.left_lane_add_vehicle.setEnabled(True)

    def delete_car(self,index,lane):
        def delete():
            self.subject_labels[index].destroy()
            self.subject_delete_buttons[index].destroy()
            self.parent_window.subject_vehicle_list[index].destroy()
            self.hide()
            self.show()
        return delete











def main():
    primary.main()


if __name__ == "__main__":
    main()
