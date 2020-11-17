from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import freeway_window
import vehicle
import add_vehicles
import edit_vehicle
import section_vector

import home as primary



class Edit_Section_Window(QWidget):
    def __init__(self,val,freeway_window,parent=None):
        """
        edit section window for editing vehicle behavior at each freeway section
        there are n number of edit_section_window objects where n = num_sections
        """
        super(Edit_Section_Window, self).__init__(parent)
        self.setGeometry(0,0,primary.width,primary.height)
        self.section_index = val
        self.freeway_window = freeway_window
        self.initUI()


    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setContentsMargins(0,0,0,0)


        #title text
        self.section_text = QLabel()
        self.section_text.setText("Edit Freeway Section")
        self.section_text.setAlignment(QtCore.Qt.AlignCenter)
        self.section_text.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.section_text.setFont(QFont("Arial", 20))
        self.section_text.setMaximumHeight(primary.height/6)
        self.section_text.setMaximumWidth(primary.width/5)


        #back button
        self.back_button = QPushButton()
        self.back_button.setText("General Settings")
        self.back_button.setFont(QFont("Arial", 16))
        self.back_button.setMaximumWidth(primary.width/10)
        self.back_button.setMaximumHeight(primary.height/26)
        self.back_button.clicked.connect(self.freeway_window.go_to_general_settings)
        self.back_button.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")

        #intersection id
        self.section_id_text = QLabel()
        self.section_id_text.setText("Section ID")
        self.section_id_text.setFont(QFont("Arial", 16))
        self.section_id_text.setMaximumHeight(primary.height/15)
        self.section_id_text.setAlignment(QtCore.Qt.AlignCenter)

        self.section_id = QComboBox()
        self.section_id.setFont(QFont("Arial", 16))
        self.section_id.setMaximumWidth(primary.width/9)
        for i in range(0,self.freeway_window.num_sections.value()):
            self.section_id.addItem("Section {}".format(i+1))
        self.section_id.currentIndexChanged.connect(self.go_to_page)

        self.view2 = QtWidgets.QListView()
        self.view2.setLayoutMode(1)
        self.view2.setBatchSize(15)
        self.section_id.setView(self.view2)


        #import settings
        self.import_settings_button = QPushButton()
        self.import_settings_button.setText("Import Settings")
        self.import_settings_button.setFont(QFont("Arial", 16))
        self.import_settings_button.clicked.connect(self.import_settings_click)
        self.import_settings_button.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")
        self.import_settings_button.setToolTip("Replaces section's vehicle behavior settings with those of the selected section.")


        self.import_settings = QComboBox()
        self.import_settings.setFont(QFont("Arial", 16))
        self.import_settings.addItem("Custom (Default)")
        for i in range(0,self.freeway_window.num_sections.value()):
            if i == self.section_index-1:
                continue
            self.import_settings.addItem("Section {}".format(i+1))

        self.view3 = QtWidgets.QListView()
        self.view3.setLayoutMode(1)
        self.view3.setBatchSize(15)
        self.import_settings.setView(self.view3)


        #map widget
        self.map_widget = QWidget()
        self.map_widget.setMinimumWidth(primary.width/3)
        self.map_widget.setMaximumWidth(primary.width/3)
        self.map_widget.setMinimumHeight(primary.height/1.4)
        self.map_widget.setMaximumHeight(primary.height/1.4)  


        #background color
        self.map_background = QLabel(self.map_widget)
        self.map_background.setStyleSheet("background-color: #cccac6;")
        self.map_background.setMinimumHeight(primary.height/1.41)
        self.map_background.setMinimumWidth(primary.width/7)
        self.map_background.move(primary.width/6,primary.height/200)
        self.map_layout = QHBoxLayout()
        self.map_background.setLayout(self.map_layout)

    
        #map
        self.pixmap = QPixmap('images/road.gif')
        self.pixmap = self.pixmap.scaledToHeight(primary.height/1.5)

        self.map1 = QLabel(self.map_widget)
        self.map1.setPixmap(self.pixmap)
        self.map_layout.addWidget(self.map1)
        self.map1.setAlignment(QtCore.Qt.AlignCenter)


        #ego vehicle
        self.ego_vehicle = vehicle.Vehicle(0,1,"","","222","180","55",self.map_background)
        self.ego_vehicle.setText("Ego")
        self.ego_vehicle.setFont(QFont("Arial", 10))
        self.ego_vehicle.move(self.map_background.width()/1.48,primary.height/3.06)
        self.ego_vehicle.clicked.connect(self.show_edit_ego_vehicle)
        self.ego_vehicle.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")

        #bottom spacer
        self.spacer = QLabel()
        self.spacer.setMaximumHeight(primary.height/8)


        #right side spacer
        self.spacer2 = QLabel()
        self.spacer2.setMaximumWidth(primary.width/3)
        self.spacer2.setMinimumWidth(primary.width/15)


        #add vehicles button
        self.add_vehicles = QPushButton()
        self.add_vehicles.setText("Add Vehicles")
        self.add_vehicles.setFont(QFont("Arial", 16))
        self.add_vehicles.clicked.connect(self.freeway_window.show_add_vehicles)
        self.add_vehicles.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")

        #EDIT EGO VEHICLE WINDOW
        self.edit_vehicle_window = edit_vehicle.Edit_Vehicle_Widget(self)
        self.edit_vehicle_window.hide()


        #EDIT VEHICLE WINDOWS
        self.edit_vehicle_list = list()


        #VEHICLE OBJECTS
        self.vehicle_list = list()


        #VEHICLE COUNTS (for copy_map_to_sections())
        self.subject_lead_count = 0
        self.subject_follow_count = 0
        self.left_lead_count = 0
        self.left_follow_count = 0

        

        #GRID SETTINGS
        self.grid.addWidget(self.back_button,             0,0,1,1)
        self.grid.addWidget(self.section_text,            1,0,1,2)
        self.grid.addWidget(self.section_id_text,         2,0,1,1)
        self.grid.addWidget(self.section_id,              2,1,1,1)
        self.grid.addWidget(self.add_vehicles,            3,0,1,1)
        self.grid.addWidget(self.spacer,                  4,0,1,1)
        self.grid.addWidget(self.import_settings_button,  5,0,1,1)
        self.grid.addWidget(self.import_settings,         5,1,1,1) 
        
        self.grid.addWidget(self.map_widget,              1,2,5,1)
        self.grid.addWidget(self.spacer2,                 2,3,1,1)


        
    def go_to_page(self):
        """
        connected: self.section_id.changed
        function: switches edit_section page to whichever page is specified by section_id change
        """

        next_page_index = int(self.section_id.currentText()[8:])
        self.freeway_window.go_to_page(next_page_index)


    def show_edit_ego_vehicle(self):
        """
        connected: self.ego_vehicle.clicked
        function: opens the edit_ego_vehicle.py page to edit the ego vehicle
        """

        self.freeway_window.edit_ego_vehicle.show()
        self.freeway_window.edit_ego_vehicle.raise_()


    def import_settings_click(self):
        """
        connected: self.import_settings_button.clicked
        function: imports all behavioral settings from the specified section into this section
        """

        #if importing from self, do nothing
        if self.import_settings.currentIndex() == 0:
            return
        
        #number of vehicles in simulation
        num_cars = len(self.freeway_window.add_vehicles_widget.subject_vehicle_list)+len(self.freeway_window.add_vehicles_widget.left_vehicle_list)

        #page to import from
        import_index = int(self.import_settings.currentText()[8:])
        import_page = section_vector.page_list[import_index]

        #copy all data from page that we are importing from and put into tuple list
        tuple_list = list()
        for i in range(0,num_cars):
            car_index_input = import_page.edit_vehicle_list[i].car_index
            vary_speed_input = import_page.edit_vehicle_list[i].vary_speed_button.isChecked()
            lane_change_input = import_page.edit_vehicle_list[i].lane_change_yes.isChecked()
            lane_change_time_input = import_page.edit_vehicle_list[i].lane_change_time.value()
            safety_distance_input = import_page.edit_vehicle_list[i].safety_distance.value()
            tupl = tuple((car_index_input,vary_speed_input,lane_change_input,lane_change_time_input,safety_distance_input))
            tuple_list.append(tupl)

        #set all current data to data which we have imported
        for i in range(0,num_cars):
            if tuple_list[i][1] == True:
                self.edit_vehicle_list[i].vary_speed_button.setChecked(True)
            if tuple_list[i][2] == True:
                self.edit_vehicle_list[i].lane_change_yes.setChecked(True)
                self.edit_vehicle_list[i].lane_change_time.setDisabled(False)
                self.edit_vehicle_list[i].lane_change_time_text.setDisabled(False)
            
            self.edit_vehicle_list[i].lane_change_time.setValue(tuple_list[i][3])
            self.edit_vehicle_list[i].safety_distance.setValue(tuple_list[i][4])






        




def main():
    primary.main()


if __name__ == "__main__":
    main()
