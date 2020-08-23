from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import sys
import edit_section
import drop_down_window_add
import drop_down_window_edit
import vehicle
import carla_vehicle_list

import home as primary



class Add_Vehicles_Window(QWidget):
    """
    Add vehicles page. Used to create vehicle objects to copy to edit_section.py
    """
    def __init__(self,freeway_window,parent=None):
        super(Add_Vehicles_Window, self).__init__(parent)
        self.setGeometry(0,0,primary.width,primary.height)
        self.freeway_window = freeway_window
        self.initUI()


    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setContentsMargins(0,0,0,0)
        self.setAutoFillBackground(True)



        #back button
        self.back_button = QPushButton()
        self.back_button.setText("Back")
        self.back_button.setFont(QFont("Arial", 16))
        self.back_button.setMaximumWidth(primary.width/10)
        self.back_button.setMaximumHeight(primary.height/26)
        self.back_button.clicked.connect(self.freeway_window.add_vehicle_edit_windows) 
        self.back_button.clicked.connect(self.freeway_window.copy_map_to_sections)   
        self.back_button.clicked.connect(self.freeway_window.hide_add_vehicles)
        

        #map widget
        self.map_widget = QWidget()
        self.map_widget.setMinimumWidth(primary.width/3)
        self.map_widget.setMaximumWidth(primary.width/3)
        self.map_widget.setMinimumHeight(primary.height/1.3)
        self.map_widget.setMaximumHeight(primary.height/1.3)
        

        #background color
        self.map_background = QLabel(self.map_widget)
        self.map_background.setStyleSheet("background-color: #cccac6;")
        self.map_background.setMinimumHeight(primary.height/1.41)
        self.map_background.setMinimumWidth(primary.width/7)
        self.map_background.move( primary.width/26,primary.height/70)
        self.map_layout = QHBoxLayout()
        self.map_background.setLayout(self.map_layout)


        #map
        self.pixmap = QPixmap('images/road.gif')
        self.pixmap = self.pixmap.scaledToHeight(primary.height/1.5)

        self.map1 = QLabel(self.map_widget)
        self.map1.setPixmap(self.pixmap)
        self.map1.setAlignment(QtCore.Qt.AlignCenter)
        self.map_layout.addWidget(self.map1)


        #ego vehicle
        self.ego_vehicle = vehicle.Vehicle(0,1,"","","222","180","55",self.map_background)
        self.ego_vehicle.setText("Ego")
        self.ego_vehicle.setFont(QFont("Arial", 10))
        self.ego_vehicle.move(self.map_background.width()/1.48,primary.height/2.98)


        #right side spacer
        self.spacer = QLabel()
        self.spacer.setMaximumHeight(primary.height/4)
        self.spacer.setMaximumWidth(primary.width/2)
        self.spacer.setMinimumWidth(primary.width/2)


        #bottom spacer
        self.spacer_bottom = QLabel()
        self.spacer_bottom.setMaximumWidth(primary.width/3)
        self.spacer_bottom.setMinimumWidth(primary.width/15)



        #ADD VEHICLES
        
            #add vehicle widget
        self.add_vehicles_widget = QWidget()

        self.add_vehicles_widget.setMaximumHeight(primary.height/1.5)
        self.add_vehicles_widget.setMinimumHeight(primary.height/1.5)
        self.add_vehicles_widget.setMinimumWidth(primary.width/2.5)        
        self.add_vehicles_widget.setMaximumWidth(primary.width/2.5)


            #background color
        self.background = QLabel(self.add_vehicles_widget)
        self.background.setMinimumWidth(self.add_vehicles_widget.width())
        self.background.setMinimumHeight(self.add_vehicles_widget.height())
        self.background.setAutoFillBackground(True)


            #add vehicles title
        self.add_vehicles_title = QLabel(self.add_vehicles_widget)
        self.add_vehicles_title.setText("Add Vehicles")
        self.add_vehicles_title.setFont(QFont("Arial", 20))
        self.add_vehicles_title.move(primary.width/11,primary.height/10)


            #subject lane
        self.subject_lane_text = QLabel(self.add_vehicles_widget)
        self.subject_lane_text.setText("Subject Lane")
        self.subject_lane_text.setFont(QFont("Arial",18))
        self.subject_lane_text.setFrameStyle(1)
        self.subject_lane_text.setAlignment(QtCore.Qt.AlignCenter)
        self.subject_lane_text.setMinimumWidth(primary.width/12)
        self.subject_lane_text.move(primary.width/25,primary.height/4.9)


            #add vehicle
        self.subject_lane_add_vehicle = QPushButton(self.add_vehicles_widget)
        self.subject_lane_add_vehicle.setText("Add Vehicle")
        self.subject_lane_add_vehicle.setFont(QFont("Arial",16))
        self.subject_lane_add_vehicle.setMinimumWidth(primary.width/10)
        self.subject_lane_add_vehicle.move(primary.width/6,primary.height/5)
        self.subject_lane_add_vehicle.clicked.connect(self.add_vehicle_subject_lane_click)


            #left lane
        self.left_lane_text = QLabel(self.add_vehicles_widget)
        self.left_lane_text.setText("Left Lane")
        self.left_lane_text.setFont(QFont("Arial",18))
        self.left_lane_text.setFrameStyle(1)
        self.left_lane_text.setAlignment(QtCore.Qt.AlignCenter)
        self.left_lane_text.setMinimumWidth(primary.width/12)
        self.left_lane_text.move(primary.width/25,primary.height/2.5)


                #add vehicle
        self.left_lane_add_vehicle = QPushButton(self.add_vehicles_widget)
        self.left_lane_add_vehicle.setText("Add Vehicle")
        self.left_lane_add_vehicle.setFont(QFont("Arial",16))
        self.left_lane_add_vehicle.setMinimumWidth(primary.width/10)
        self.left_lane_add_vehicle.move(primary.width/6,primary.height/2.5)
        self.left_lane_add_vehicle.clicked.connect(self.add_vehicle_left_lane_click)



        #GRID SETTINGS
        self.grid.addWidget(self.back_button,             0,0,1,1)
        self.grid.addWidget(self.add_vehicles_widget,     1,0,1,1)
        self.grid.addWidget(self.spacer,                  1,2,-1,-1)
        self.grid.addWidget(self.spacer_bottom,           2,1,-1,-1)
        self.grid.addWidget(self.map_widget,              1,1,-1,-1)


        #VEHICLE LISTS
        self.all_vehicles_list = list()

        self.subject_vehicle_list = list()
        self.left_vehicle_list = list()

        self.subject_lead_gaps = list()
        self.subject_follow_gaps = list()

        self.left_lead_gaps = list()
        self.left_follow_gaps = list()
        
    


    def hide_add_vehicles(self):
        """
        connected to: self.back_button.clicked
        function: hides add_vehicles widget
        """

        self.add_vehicles_widget.hide()


    def add_vehicle_subject_lane_click(self):
        """
        connected to: self.subject_lane_add_vehicle.clicked
        function: opens up drop_down_window_add.py widget to add vehicles to subject lane
        """

        self.add_widget_subject = drop_down_window_add.Drop_Down_Window_Add("subject",self)
        self.add_widget_subject.show()
        self.add_widget_subject.move(primary.width/6,primary.height/4)


    def add_vehicle_left_lane_click(self):
        """
        connected to: self.left_lane_add_vehicle.clicked
        function: opens up drop_down_window_add.py widget to add vehicles to left lane
        """

        self.add_widget_left = drop_down_window_add.Drop_Down_Window_Add("left",self)
        self.add_widget_left.show()
        self.add_widget_left.move(primary.width/6,primary.height/2.5)


    def add_vehicle_subject(self):
        """
        connected to: drop_down_window_add-->add_button.clicked
        function: adds vehicle to the subject lane with the specified gap, color, model, and lead/follow value
        """

        #retrieve vehicle information to feed into vehicle creation
        gap = self.add_widget_subject.gap.value()
        lead_follow = self.add_widget_subject.vehicle_type.currentIndex()
        color_r = self.add_widget_subject.vehicle_color_r.value()
        color_g = self.add_widget_subject.vehicle_color_g.value()
        color_b = self.add_widget_subject.vehicle_color_b.value()
        model = self.add_widget_subject.vehicle_model.currentText()
        model_val = carla_vehicle_list.vehicle_list[model]
        color_rgb = f'{color_r},{color_g},{color_b}'
        lead_string = "lead"
        if lead_follow == 1:
            lead_string = "follow"
        
        
        #create vehicle with the following settings
        self.car = vehicle.Vehicle("subject",lead_follow,gap,model,color_r,color_g,color_b,self.map_background)

        #top and bottom of map so that vehicle canot go off of map
        top_of_map = self.car.height()/2
        bottom_of_map = self.map_background.height() - (self.car.height() * 1.5)

        
        if lead_follow == 1: #if follow vehicle
            if not self.subject_follow_gaps: #if no cars in subject follow lane
                car_placement = primary.height/3.1 + self.car.length + gap*8
                if car_placement > bottom_of_map:
                    return

                self.car.move(self.map_background.width()/1.48,car_placement)
                self.subject_follow_gaps.append(car_placement)
                self.car.position = 0 #position 0 = first follow car in subject lane

            else:
                if len(self.subject_follow_gaps) == 2: #only allow 2 vehicles per lane
                    return
                else:
                    car_placement = self.subject_follow_gaps[-1] + self.car.length + gap*5
                    if car_placement > bottom_of_map:
                        return

                    self.car.move(self.map_background.width()/1.48,car_placement)
                    self.subject_follow_gaps.append(car_placement)
                    self.car.position = 1 #position 1 = second follow car in subject lane


        else: #if lead vehicle
            if not self.subject_lead_gaps: #if no cars in subject lead lane
                car_placement = primary.height/3.1 - self.car.length/2 - gap*8
                if car_placement < top_of_map:
                    return

                self.car.move(self.map_background.width()/1.48, car_placement)
                self.subject_lead_gaps.append(car_placement)
                self.car.position = 0

            else:
                if len(self.subject_lead_gaps) == 2: #only allow 2 vehicles per lane
                    return
                else:
                    car_placement = self.subject_lead_gaps[-1] - self.car.length - gap*5
                    if car_placement < top_of_map:
                        return

                    self.car.move(self.map_background.width()/1.48, car_placement)
                    self.subject_lead_gaps.append(car_placement)
                    self.car.position = 1

        #add vehicle to appropraite vehicle lists
        self.subject_vehicle_list.append(self.car)
        self.car.setText("{}".format(len(self.left_vehicle_list)+len(self.subject_vehicle_list)))
        self.car.setAlignment(QtCore.Qt.AlignCenter)
        self.car.setObjectName("car") #set vehicle object name for future referene
        self.all_vehicles_list.append(self.car)
        self.car.show()

        #create vehicle in CARLA simulation
        carla_car = self.parent().freewayenv.add_full_path_vehicle(gap = gap, model_name=model_val, vehicle_type =lead_string, 
                                                            choice = "subject",vehicle_color=color_rgb)

        #add vehicle to carla vehicle list for later use
        if lead_string == "lead":
            self.parent().carla_vehicle_list_subject_lead.append(carla_car)
        else:
            self.parent().carla_vehicle_list_subject_follow.append(carla_car)


    def add_vehicle_left(self):
        """
        connected to: drop_down_window_add-->add_button.clicked
        function: adds vehicle to the left lane with the specified gap, color, model, and lead/follow value
        """

        #retrieve vehicle information to feed into vehicle creation
        gap = self.add_widget_left.gap.value()
        gap = int(gap)
        lead_follow = self.add_widget_left.vehicle_type.currentIndex()
        color_r = self.add_widget_left.vehicle_color_r.value()
        color_g = self.add_widget_left.vehicle_color_g.value()
        color_b = self.add_widget_left.vehicle_color_b.value()
        model = self.add_widget_left.vehicle_model.currentText()
        model_val = carla_vehicle_list.vehicle_list[model]
        color_rgb = f'{color_r},{color_g},{color_b}'
        lead_string = "lead"
        if lead_follow == 1:
            lead_string = "follow"
        
        #create vehicle with the following settings
        self.car = vehicle.Vehicle("left",lead_follow,gap,model,color_r,color_g,color_b,self.map_background)

        #top and bottom values so vehicle cannot be placed outside of map
        top_of_map = self.car.height()/2
        bottom_of_map = self.map_background.height() - (self.car.height() * 1.5)


        if lead_follow == 1:#if follow vehicle
            if not self.left_follow_gaps: #if no cars in subject follow lane
                car_placement = primary.height/3.1 + self.car.length + gap*8
                if car_placement > bottom_of_map:
                    return

                self.car.move(self.map_background.width()/1.77, car_placement)
                self.left_follow_gaps.append(car_placement)
                self.car.position = 0

            else:
                if len(self.left_follow_gaps) == 2: #only allow 2 vehicles per lane
                    return
                else:
                    car_placement = self.left_follow_gaps[-1] + self.car.length + gap*5
                    if car_placement > bottom_of_map:
                        return

                    self.car.move(self.map_background.width()/1.77,car_placement)
                    self.left_follow_gaps.append(car_placement)
                    self.car.position = 1

        else:#if lead vehicle
            if not self.left_lead_gaps: #if no cars in subject lead lane
                car_placement = primary.height/3.1 - self.car.length/2 - gap*8
                if car_placement < top_of_map:
                    return

                self.car.move(self.map_background.width()/1.77, car_placement)
                self.left_lead_gaps.append(car_placement)
                self.car.position = 0

            else:
                if len(self.left_lead_gaps) == 2: #only allow 2 vehicles per lane
                    return
                else:
                    car_placement = self.left_lead_gaps[-1] - self.car.length - gap*5
                    if car_placement < top_of_map:
                        return

                    self.car.move(self.map_background.width()/1.77, car_placement)
                    self.left_lead_gaps.append(car_placement)
                    self.car.position = 1

        #add vehicles to appropriate lists for later reference
        self.left_vehicle_list.append(self.car)
        self.car.setText("{}".format(len(self.left_vehicle_list)+len(self.subject_vehicle_list)))
        self.car.setObjectName("car")
        self.all_vehicles_list.append(self.car)
        self.car.show()

        #create vehicle in CARLA environment
        carla_car = self.parent().freewayenv.add_full_path_vehicle(gap = gap, model_name=model_val, vehicle_type =lead_string, 
                                                            choice = "left",vehicle_color=color_rgb)

        #add vehicle to CARLA vehicle list 
        if lead_string == "lead":
            self.parent().carla_vehicle_list_left_lead.append(carla_car)
        else:
            self.parent().carla_vehicle_list_left_follow.append(carla_car)
        


        




def main():
    primary.main()


if __name__ == "__main__":
    main()