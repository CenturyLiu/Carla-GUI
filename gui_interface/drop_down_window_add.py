from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import edit_section
import freeway_window
import home as primary
import carla_vehicle_list



class Drop_Down_Window_Add(QDialog):
    """
    Drop down window used to add vehicles to add_vehicles.py
    """
    def __init__(self,lane,parent=None):
        super(Drop_Down_Window_Add, self).__init__(parent)
        self.parent_window = parent
        self.lane = lane
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setWindowTitle("Add Vehicle")
        self.grid.setContentsMargins(0,10,0,0)

        #dimensions
        self.setMinimumHeight(primary.height/3)
        self.setMinimumWidth(primary.width/8)
        self.setMaximumHeight(primary.height/3)
        self.setMaximumWidth(primary.width/8)


        #close button
        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.clicked.connect(self.close)


        #gap size
        self.gap_text = QLabel()
        self.gap_text.setText("Gap (m)")

        self.gap = QSpinBox()
        self.gap.setMaximumWidth(primary.width/30)
        self.gap.setMaximumHeight(primary.height/30)
        self.gap.setAlignment(QtCore.Qt.AlignCenter)
        self.gap.setMinimum(8)
        self.gap.setValue(10)
        self.gap.setMaximum(35)


        #vehicle model
        self.vehicle_model_text = QLabel()
        self.vehicle_model_text.setText("Model")

        self.vehicle_model = QComboBox()
        for vehicle in carla_vehicle_list.vehicle_list:
            self.vehicle_model.addItem(vehicle)


        #vehicle type 
        self.vehicle_type_text = QLabel()
        self.vehicle_type_text.setText("Type")

        self.vehicle_type = QComboBox()
        self.vehicle_type.addItem("Lead")
        self.vehicle_type.addItem("Follow")


        #vehicle color
        self.vehicle_color_text = QLabel()
        self.vehicle_color_text.setText("Color (RGB)")

        self.vehicle_color = QWidget()
        self.horiz_layout = QHBoxLayout()
        self.vehicle_color.setLayout(self.horiz_layout)

        self.vehicle_color_r = QSpinBox()
        self.vehicle_color_g = QSpinBox()
        self.vehicle_color_b = QSpinBox()

        self.vehicle_color_r.setAlignment(QtCore.Qt.AlignCenter)
        self.vehicle_color_g.setAlignment(QtCore.Qt.AlignCenter)
        self.vehicle_color_b.setAlignment(QtCore.Qt.AlignCenter)

        self.vehicle_color_r.setMinimumWidth(primary.width/50)
        self.vehicle_color_r.setMaximumHeight(primary.height/30)
        self.vehicle_color_g.setMinimumWidth(primary.width/50)
        self.vehicle_color_g.setMaximumHeight(primary.height/30)
        self.vehicle_color_b.setMinimumWidth(primary.width/50)
        self.vehicle_color_b.setMaximumHeight(primary.height/30)

        self.vehicle_color_r.setFont(QFont("Arial", 9))
        self.vehicle_color_g.setFont(QFont("Arial", 9))
        self.vehicle_color_b.setFont(QFont("Arial", 9))

        self.vehicle_color_r.setMaximum(255)
        self.vehicle_color_r.setMinimum(0)
        self.vehicle_color_g.setMaximum(255)
        self.vehicle_color_g.setMinimum(0)
        self.vehicle_color_b.setMaximum(255)
        self.vehicle_color_b.setMinimum(0)

        self.vehicle_color_r.setValue(255)
        self.vehicle_color_g.setValue(255)
        self.vehicle_color_b.setValue(255)

        self.horiz_layout.addWidget(self.vehicle_color_r)
        self.horiz_layout.addWidget(self.vehicle_color_g)
        self.horiz_layout.addWidget(self.vehicle_color_b)


        #add button
        self.add_button = QPushButton()
        self.add_button.setText("Add")
        if self.lane == "left":
            self.add_button.clicked.connect(self.parent_window.add_vehicle_left)
        else:
            self.add_button.clicked.connect(self.parent_window.add_vehicle_subject)
        


        #GRID SETTINGS
        #self.grid.addWidget(self.close_button, 0,0,1,2) close button removed from grid and move() function used instead
        self.grid.addWidget(self.gap_text, 1,0,1,1)
        self.grid.addWidget(self.gap, 1,1,1,1)
        self.grid.addWidget(self.vehicle_model_text, 2,0,1,1)
        self.grid.addWidget(self.vehicle_model, 2,1,1,1)
        self.grid.addWidget(self.vehicle_type_text, 3,0,1,1)
        self.grid.addWidget(self.vehicle_type, 3,1,1,1)
        self.grid.addWidget(self.vehicle_color_text, 4,0,1,1)
        self.grid.addWidget(self.vehicle_color, 4,1,1,1)
        self.grid.addWidget(self.add_button, 5,0,1,2)
        
        


    def close(self):
        """
        connected: self.close_button.clicked
        function: closes the drop down window to add vehicles -- reenables disabled buttons 
        """
        self.hide()
        self.parent_window.hide()
        self.parent_window.show()
        self.parent_window.subject_lane_add_vehicle.setEnabled(True)
        self.parent_window.subject_lane_edit_lane.setEnabled(True)

        











def main():
    primary.main()


if __name__ == "__main__":
    main()