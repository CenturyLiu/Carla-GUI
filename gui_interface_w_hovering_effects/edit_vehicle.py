from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import freeway_window
import vehicle
import add_vehicles
import section_vector
import carla_vehicle_list

import home as primary

class Edit_Vehicle_Widget(QFrame):
    """
    QFrame object to edit each vehicle
    This object will appear when clicking on any vehicle in edit_section.py
    """
    def __init__(self,car_index,parent=None):
        super(Edit_Vehicle_Widget, self).__init__(parent)
        self.parent_window = parent
        self.car_index = car_index
        self.initUI()


    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setContentsMargins(15,15,0,0)

        #set frame border
        self.setFrameStyle(1)
        self.setAutoFillBackground(True)

        #dimensions
        self.setMinimumWidth(primary.width/3.5)
        self.setMaximumHeight(primary.height)
        self.setMinimumHeight(primary.height)
        self.setMaximumWidth(primary.width/3.5)


        #close button
        self.close_button = QPushButton()
        self.close_button.setText("Close")
        self.close_button.setMaximumWidth(primary.width/15)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")

        #title text
        self.title_text = QLabel()
        self.title_text.setText("Edit Vehicle {}".format(self.car_index))
        self.title_text.setFont(QFont("Arial", 20))
        self.title_text.setMaximumHeight(primary.height/20)
        self.title_text.setAlignment(QtCore.Qt.AlignHCenter)

        
        #vehicle model
        self.vehicle_model_text = QLabel()
        self.vehicle_model_text.setText("Model")

        self.vehicle_model = QComboBox()
        for vehicle in carla_vehicle_list.vehicle_list:
            self.vehicle_model.addItem(vehicle)
        

        #vary speed by range
        self.vary_speed_range_text = QLabel()
        self.vary_speed_range_text.setText("Vary Speed by Range")
        self.vary_speed_range_text.setMaximumHeight(primary.height/20)

        self.vary_speed_button = QRadioButton()
        self.vary_speed_button.setStyleSheet("margin-left:50%; margin-right:50%;")


        #maintain max speed test
        self.maintain_max_speed_text = QLabel()
        self.maintain_max_speed_text.setText("Maintain Max Speed")
        self.maintain_max_speed_text.setMaximumHeight(primary.height/20)

        self.maintain_speed_button = QRadioButton()
        self.maintain_speed_button.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.maintain_speed_button.setChecked(True)


        #lane change   
        self.lane_change_text = QLabel()
        self.lane_change_text.setText("Lane Change")

        self.lane_change_no = QRadioButton()
        self.lane_change_no.setText("No")
        self.lane_change_no.setChecked(True)
        self.lane_change_no.clicked.connect(self.lane_no_click)
        self.lane_change_no.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")
        
        self.lane_change_yes = QRadioButton()
        self.lane_change_yes.setText("Yes")
        self.lane_change_yes.clicked.connect(self.lane_yes_click)
        self.lane_change_yes.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")
        
        self.lane_change_widget = QWidget()
        self.lane_change_grid = QHBoxLayout()

        self.lane_change_widget.setLayout(self.lane_change_grid)
        self.lane_change_widget.setMaximumHeight(primary.height/8)

        self.lane_change_grid.addWidget(self.lane_change_yes)
        self.lane_change_grid.addWidget(self.lane_change_no)


        #lane change time
        self.lane_change_time_text = QLabel()
        self.lane_change_time_text.setText("Lane Change Time (s)")
        self.lane_change_time_text.setDisabled(True)

        self.lane_change_time = QSpinBox()
        self.lane_change_time.setMaximumHeight(primary.height/25)
        self.lane_change_time.setMaximumWidth(primary.width/25)
        self.lane_change_time.setAlignment(QtCore.Qt.AlignCenter)
        self.lane_change_time.setDisabled(True)
        self.lane_change_time.setMinimum(0)
        self.lane_change_time.setMaximum(10)
        self.lane_change_time.setValue(5)


        #safety distance
        self.safety_distance_text = QLabel()
        self.safety_distance_text.setText("Safety Distance (m)")

        self.safety_distance = QSpinBox()
        self.safety_distance.setMaximumHeight(primary.height/25)
        self.safety_distance.setMaximumWidth(primary.width/25)
        self.safety_distance.setAlignment(QtCore.Qt.AlignCenter)
        self.safety_distance.setMinimum(5)
        self.safety_distance.setMaximum(999)
        self.safety_distance.setValue(10)


        #delete button
        self.delete_button = QPushButton()
        self.delete_button.setText("Delete")
        self.delete_button.setMaximumWidth(primary.width/15)
        self.delete_button.clicked.connect(self.car_delete)
        self.delete_button.setStyleSheet("QPushButton::hover"
        "{"
        "background-color : lightblue;"
        "}")

        #vehicle color
        self.vehicle_color_text = QLabel()
        self.vehicle_color_text.setText("Color (RGB)")

        self.vehicle_color = QWidget()
        self.horiz_layout = QHBoxLayout()
        self.vehicle_color.setLayout(self.horiz_layout)
        self.vehicle_color.setMaximumHeight(primary.height/12)

        self.vehicle_color_r = QSpinBox()
        self.vehicle_color_g = QSpinBox()
        self.vehicle_color_b = QSpinBox()

        self.vehicle_color_r.setAlignment(QtCore.Qt.AlignCenter)
        self.vehicle_color_g.setAlignment(QtCore.Qt.AlignCenter)
        self.vehicle_color_b.setAlignment(QtCore.Qt.AlignCenter)

        self.vehicle_color_r.setMinimumWidth(primary.width/30)
        self.vehicle_color_r.setMaximumHeight(primary.height/30)
        self.vehicle_color_g.setMinimumWidth(primary.width/30)
        self.vehicle_color_g.setMaximumHeight(primary.height/30)
        self.vehicle_color_b.setMinimumWidth(primary.width/30)
        self.vehicle_color_b.setMaximumHeight(primary.height/30)

        self.vehicle_color_r.setFont(QFont("Arial", 12))
        self.vehicle_color_g.setFont(QFont("Arial", 12))
        self.vehicle_color_b.setFont(QFont("Arial", 12))

        self.vehicle_color_r.setMinimum(0)
        self.vehicle_color_r.setMaximum(255)
        self.vehicle_color_g.setMinimum(0)
        self.vehicle_color_g.setMaximum(255)
        self.vehicle_color_b.setMinimum(0)
        self.vehicle_color_b.setMaximum(255)

        self.vehicle_color_r.setValue(255)
        self.vehicle_color_g.setValue(255)
        self.vehicle_color_b.setValue(255)

        self.horiz_layout.addWidget(self.vehicle_color_r)
        self.horiz_layout.addWidget(self.vehicle_color_g)
        self.horiz_layout.addWidget(self.vehicle_color_b)


        #spacer
        self.spacer = QWidget()
        self.spacer.setMaximumHeight(primary.height/15)


        #spacer 2
        self.spacer2 = QLabel()
        self.spacer2.setMaximumHeight(primary.height/10)



        #GRID SETTINGS
        self.grid.addWidget(self.close_button,             0,0,1,1)       
        self.grid.addWidget(self.title_text,               1,0,1,3)
        self.grid.addWidget(self.vehicle_model_text,       2,0,1,1)
        self.grid.addWidget(self.vehicle_model,            2,1,1,1)
        self.grid.addWidget(self.vary_speed_range_text,    3,0,1,1)
        self.grid.addWidget(self.maintain_max_speed_text,  3,1,1,1)
        self.grid.addWidget(self.vary_speed_button,        4,0,1,1)
        self.grid.addWidget(self.maintain_speed_button,    4,1,1,1)
        self.grid.addWidget(self.lane_change_text,         5,0,1,1)
        self.grid.addWidget(self.lane_change_widget,       5,1,1,2)
        self.grid.addWidget(self.lane_change_time_text,    6,0,1,1)
        self.grid.addWidget(self.lane_change_time,         6,1,1,2)
        self.grid.addWidget(self.safety_distance_text,     7,0,1,1)
        self.grid.addWidget(self.safety_distance,          7,1,1,2)
        self.grid.addWidget(self.vehicle_color_text,       8,0,1,1)
        self.grid.addWidget(self.vehicle_color,            8,1,1,1)
        self.grid.addWidget(self.delete_button,            9,0,1,1)
        self.grid.addWidget(self.spacer2,                  10,0,1,1)
        



    def close(self):
        """
        connected: self.close_button.clicked
        function: applies all edits made to clicked vehicle on the vehicle map and in the CARLA environment
        """

        for car in self.parent().freeway_window.add_vehicles_widget.map_background.children(): #iterate over all cars
            if car.objectName() == "car":
                if int(car.text()) == self.car_index + 1: #if car matches this edit_page

                    r = self.vehicle_color_r.value()
                    g = self.vehicle_color_g.value()
                    b = self.vehicle_color_b.value()
                    model = carla_vehicle_list.vehicle_list[self.vehicle_model.currentText()]
                    
                    if car.lane == "subject" and car.lead: # if subject and follow
                        vehicle = self.parent().freeway_window.freewayenv.edit_full_path_vehicle_init_setting( #make edit in carla simulation
                            uniquename=  self.parent().freeway_window.carla_vehicle_list_subject_follow[car.position],
                            vehicle_type= 'follow',
                            choice= 'subject',
                            model_name= model,
                            safety_distance= self.safety_distance.value(),
                            vehicle_color= f'{r},{g},{b}'
                        )
                        self.parent().freeway_window.carla_vehicle_list_subject_follow.pop(car.position)
                        self.parent().freeway_window.carla_vehicle_list_subject_follow.insert(car.position,vehicle)


                    if car.lane == "subject" and not car.lead: #if subject and lead
                        vehicle = self.parent().freeway_window.freewayenv.edit_full_path_vehicle_init_setting( #make edit in carla simulation
                            uniquename=  self.parent().freeway_window.carla_vehicle_list_subject_lead[car.position],
                            vehicle_type= 'lead',
                            choice= 'subject',
                            model_name= model,
                            safety_distance= self.safety_distance.value(),
                            vehicle_color= f'{r},{g},{b}'
                        )
                        self.parent().freeway_window.carla_vehicle_list_subject_lead.pop(car.position)
                        self.parent().freeway_window.carla_vehicle_list_subject_lead.insert(car.position,vehicle)


                    if car.lane == "left" and car.lead: #if left and follow
                        vehicle = self.parent().freeway_window.freewayenv.edit_full_path_vehicle_init_setting( #make edit in carla simulation
                            uniquename=  self.parent().freeway_window.carla_vehicle_list_left_follow[car.position],
                            vehicle_type= 'follow',
                            choice= 'left',
                            model_name= model,
                            safety_distance= self.safety_distance.value(),
                            vehicle_color= f'{r},{g},{b}'
                        )
                        self.parent().freeway_window.carla_vehicle_list_left_follow.pop(car.position)
                        self.parent().freeway_window.carla_vehicle_list_left_follow.insert(car.position,vehicle)


                    if car.lane == "left" and not car.lead:#if left and lead
                        vehicle = self.parent().freeway_window.freewayenv.edit_full_path_vehicle_init_setting( #make edit in carla simulation
                            uniquename=  self.parent().freeway_window.carla_vehicle_list_left_lead[car.position],
                            vehicle_type= 'lead',
                            choice= 'left',
                            model_name= model,
                            safety_distance= self.safety_distance.value(),
                            vehicle_color= f'{r},{g},{b}'
                        )
                        self.parent().freeway_window.carla_vehicle_list_left_lead.pop(car.position)
                        self.parent().freeway_window.carla_vehicle_list_left_lead.insert(car.position,vehicle)
                        
                    car.change_color(r,g,b) #change color of vehicle


        self.copy_color_and_model_to_sections() #copy color and model settings to all vehicle sections
        
        self.hide()
        self.parent().hide()
        self.parent().show()

    def copy_color_and_model_to_sections(self):
        """
        connected: none
        function: called by close() function
        this function will copy the color and model of all vehicles from add_vehicles.py to all sections of edit_section.py
        this allows for the color of each car on the map to be the same as the vehicles in the CARLA simulation
        """

        #number of vehicles
        num_vehicles = len(self.parent().freeway_window.add_vehicles_widget.all_vehicles_list)

        #all edit vehicle pages from add_vehicles.py
        car_list = self.parent().edit_vehicle_list

        tuple_list = list()
        for i in range(0,num_vehicles): #iterate over all vehicles and retrieve color and model
            index = car_list[i].car_index
            model = car_list[i].vehicle_model.currentText()
            r = car_list[i].vehicle_color_r.value()
            g = car_list[i].vehicle_color_g.value()
            b = car_list[i].vehicle_color_b.value()
            tupl = tuple((index,model,r,g,b))
            tuple_list.append(tupl)

        for page in range(1,len(section_vector.page_list)): #iterate over all sections 
            for i in range(0,num_vehicles): #iterate over all vehicles 
                edit_page = section_vector.page_list[page].edit_vehicle_list[i]

                edit_page.vehicle_model.setCurrentText(tuple_list[i][1]) #set text 
                edit_page.vehicle_color_r.setValue(tuple_list[i][2]) #set edit_vehicle.py color
                edit_page.vehicle_color_g.setValue(tuple_list[i][3])
                edit_page.vehicle_color_b.setValue(tuple_list[i][4])

                car = section_vector.page_list[page].vehicle_list[i]
                car.change_color(tuple_list[i][2],tuple_list[i][3],tuple_list[i][4]) #set vehicle color


    def lane_no_click(self):
        """
        connected: self.lane_change_no.clicked
        function: disables lane change time option if no lane change is selected
        """

        self.lane_change_time.setDisabled(True)
        self.lane_change_time_text.setDisabled(True)

    def lane_yes_click(self):
        """
        connected: self.lane_change_yes.clicked
        function: enables lane change time option if lane change is selected
        """

        self.lane_change_time.setDisabled(False)
        self.lane_change_time_text.setDisabled(False)


    #BROKEN
    def car_delete(self):
        """
        connected: self.delete_button.clicked
        function: deletes vehicle
        THIS FUNCTION IS BROKEN AND NEEDS TO BE CORRECTLY IMPLEMENTED
        """

        
        #remove from add_vehicles widget
        for car in self.parent().freeway_window.add_vehicles_widget.map_background.children():
            if car.objectName() == "car":
                if int(car.text()) == self.car_index + 1:

                    if car.lane == "subject":
                        self.parent().freeway_window.add_vehicles_widget.subject_vehicle_list.pop()
                        if car.lead == False:
                            self.parent().freeway_window.add_vehicles_widget.subject_lead_gaps.pop(car.position)
                        else:
                            self.parent().freeway_window.add_vehicles_widget.subject_follow_gaps.pop(car.position)
                    else:
                        self.parent().freeway_window.add_vehicles_widget.left_vehicle_list.pop()
                        if car.lead == False:
                            self.parent().freeway_window.add_vehicles_widget.left_lead_gaps.pop(car.position)
                        else:
                            self.parent().freeway_window.add_vehicles_widget.left_follow_gaps.pop(car.position)
                    

                    car.setParent(None)
                    car.deleteLater()
                    car = None


        for car in self.parent().freeway_window.add_vehicles_widget.map_background.children():
            if car.objectName() == "car":
                if int(car.text()) > self.car_index + 1:
                    index = int(car.text()) - 1
                    car.setText(str(index))
        

        #remove from all edit_sections widgets
        for page in range(1,len(section_vector.page_list)):
            for car in section_vector.page_list[page].map_background.children():
                if car.objectName() == "car":
                    if int(car.text()) == self.car_index+1:
                        car.setParent(None)
                        car.deleteLater()
                        car = None

        for page in range(1,len(section_vector.page_list)):
            for car in section_vector.page_list[page].map_background.children():
                if car.objectName() == "car":
                    print(car)
                    if int(car.text()) > self.car_index + 1:
                        index = int(car.text()) - 1
                        car.setText(str(index))
        

        









def main():
    primary.main()


if __name__ == "__main__":
    main()
