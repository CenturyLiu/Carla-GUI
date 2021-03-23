from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from functools import partial
import sys
import section_vector
import add_vehicles
import vehicle
import edit_vehicle
import edit_vehicle_ego
import start_sim_pop_up
import back_home_pop_up
import gui_test as primary
import glob
import os
import sys

# Allow imports from parent and sibling directories
sys.path.append("..")
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import time
from backend.carla_env import CARLA_ENV
from backend.section_environment import FreewayEnv
from ui_helpers import ExtendedQLabel


class Freeway_Window(QMainWindow):
    """
    Window for users to set up Freeway Experiments.
    
    Enables users to choose general experiment settings and customize
    the vehicles on the roadway using an interactive map.
    """
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setGeometry(0, 0, primary.width, primary.height)
        self.setWindowTitle("Freeway Experiments")
        self.initUI() # Create the UI componenets
        
        # TODO reenable this; disabled for gui development
        # self.carla_start() # Establish connected to Carla Server


    def carla_start(self):
        """
        Establishes a connected to the Carla server.
        
        Connects to the Carla server on localhost:2000 and loads the desired
        map, weather parameters, and spectator view. If the function is unable
        to connect within 10 seconds, it times out and exits.
        """
        try:
            # Connect to the server
            client = carla.Client("localhost",2000)
            client.set_timeout(10.0)
            world = client.load_world('Town04')

            # Set the weather
            weather = carla.WeatherParameters(
                cloudiness = 10.0,
                precipitation=0.0,
                sun_altitude_angle=90.0
            )
            world.set_weather(weather)

            # Set the spectator view
            spectator = world.get_spectator()
            spectator.set_transform(
                carla.Transform(
                    carla.Location(x=-170, y=-151, z=116.5), 
                    carla.Rotation(pitch=-33, yaw= 56.9, roll=0.0)
                    )
                )   

            self.env = CARLA_ENV(world)

        finally:
            # Failed to connect, abort
            time.sleep(5)
            self.env.destroy_actors()



    def show_add_vehicles(self):
        """
        connected to: edit_section.py-->add_vehicles_button.clicked
        function: shows add_vehicles.py window when pressing add vehicles button in an edit section page
        """

        # menubar - GUI Instruction
        menubar = self.menuBar()

        # GENERAL SETTINGS
        fileMenu = menubar.addMenu('Instructions')
        gs = QMenu('GENERAL SETTINGS', self)
        gsStr1 = "1. Choose collision availability."
        gsStr2 = "2. Enter the number of Freeway Sections. (Between 1 and 7)"
        gsStr3 = "3. Enter the maximum speed. (Max: 150 m/s)"
        gsStr4 = "4. Enter the minimum speed. (Min: 0 m/s)"
        gsStr5 = "5. Enter the safety distance between cars. (Min: 5 m, Max: 999 m)"
        gsStr6 = "6. Click the number box on each section to edit. "
        gsStr7 = "* If there are more than 5 sections, click the arrow to see more."
        gsStr8 = "* You can always discard all settings and return to the main page by hitting \"Back to Start\"."
        gsAct1 = QAction(gsStr1, self)
        gsAct2 = QAction(gsStr2, self)
        gsAct3 = QAction(gsStr3, self)
        gsAct4 = QAction(gsStr4, self)
        gsAct5 = QAction(gsStr5, self)
        gsAct6 = QAction(gsStr6, self)
        gsAct7 = QAction(gsStr7, self)
        gsAct8 = QAction(gsStr8, self)
        gs.addAction(gsAct1)
        gs.addAction(gsAct2)
        gs.addAction(gsAct3)
        gs.addAction(gsAct4)
        gs.addAction(gsAct5)
        gs.addAction(gsAct6)
        gs.addAction(gsAct7)
        gs.addAction(gsAct8)    
        fileMenu.addMenu(gs)
        gs.setStyleSheet(
            "font-size: 16px;"
        )
        
        # EDIT FREEWAY SECTION
        efs = QMenu('EDIT FREEWAY SECTION', self)     
        efsStr1 = "1. Choose Section ID and hit \"Add Vehicles\"."
        efsStr2 = "2. If you'd like to copy a specific section's setting, you can choose a corresponding section ID on the bottom of the window and hit \"Copy Settings\"."
        efsStr3 = "*Example*"
        efsStr4 = "Let's say you want Section 5 to have the same settings as Section 2 does."
        efsStr5 = "Select Section ID to Section 5."
        efsStr6 = "Select Section 5 on the bottom and hit \"Copy Settings\"."
        efsAct1 = QAction(efsStr1, self)
        efsAct2 = QAction(efsStr2, self)
        efsAct3 = QAction(efsStr3, self)
        efsAct4 = QAction(efsStr4, self)
        efsAct5 = QAction(efsStr5, self)
        efsAct6 = QAction(efsStr6, self)
        efs.addAction(efsAct1)
        efs.addAction(efsAct2)
        efs.addAction(efsAct3)
        efs.addAction(efsAct4)
        efs.addAction(efsAct5)
        efs.addAction(efsAct6)      
        fileMenu.addMenu(efs)
        efs.setStyleSheet(
            "font-size: 16px;"
        )

        # ADD VEHICLES
        addV = QMenu('ADD VEHICLES', self)
        addVStr1 = "1. Add vehicles to preffered lane by hitting \"Add Vehicle\"."
        addVStr2 = "2. Enter the gap. (Min: 8 m, Max: 35 m)"
        addVStr3 = "3. Choose a vehicle model."
        addVStr4 = "4. Choose a vehicle type (lead or ego)"
        addVStr5 = "5. Choose a vehicle color. (The vehicle in the color is shown on the road)"
        addVStr6 = "6. Hit \"Add\" to add."
        addVAct1 = QAction(addVStr1, self)
        addVAct2 = QAction(addVStr2, self)
        addVAct3 = QAction(addVStr3, self)
        addVAct4 = QAction(addVStr4, self)
        addVAct5 = QAction(addVStr5, self)
        addVAct6 = QAction(addVStr6, self)
        addV.addAction(addVAct1)
        addV.addAction(addVAct2)
        addV.addAction(addVAct3)
        addV.addAction(addVAct4)
        addV.addAction(addVAct5)
        addV.addAction(addVAct6)   
        fileMenu.addMenu(addV)
        addV.setStyleSheet(
            "font-size: 16px;"
        )

        # Finish settings and start simulation
        ss = QAction("After done settings, you can start simulation!", self)
        fileMenu.addAction(ss)       

        fileMenu.setStyleSheet(
            "font-size: 16px;"
        )

        
        
        #CARLA SETTINGS
        self.stack = QStackedLayout() #stack contains freeway_window.py and all edit_section.py pages
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.stack)
        self.setCentralWidget(self.main_widget) #central widget necessary for pyqt5 to function correctly

        self.general_settings_widget = QWidget()
        self.grid = QGridLayout()
        self.general_settings_widget.setLayout(self.grid)
        self.stack.addWidget(self.general_settings_widget)
        section_vector.page_list.append(self.general_settings_widget) #adds freeway_window to page list

        self.add_vehicles_widget.show()
        

    def hide_add_vehicles(self):
        """
        connected to: add_vehicles.py-->back_button.clicked 
        function: hides the add_vehicles page upon clicking its own back button
        """

        self.add_vehicles_widget.setVisible(False)
        self.hide()
        self.show()


    def road_button_reset(self):
        """
        connected to: none
        function: helper function to reset text of road buttons to current values in road_array
        """
        
        self.road_button1.setText(str(self.road_array[0]))
        self.road_button2.setText(str(self.road_array[1]))
        self.road_button3.setText(str(self.road_array[2]))
        self.road_button4.setText(str(self.road_array[3]))
        self.road_button5.setText(str(self.road_array[4]))


    def road_button_click_helper(self,index):
        """
        connected to: none
        function: helper function that is called when pressing any road button
        this function creates the carla environment, the ego vehicle, and moves the user to the request edit section page
        """

        if index == "-": #if button display '-': do nothing
            return
        else:
            index = int(index)

        if self.num_sections.isEnabled() == True: #only create environment and spawn ego if it's first time going to edit_section
            self.freewayenv = FreewayEnv(self.env,self.num_sections.value())
            self.freewayenv.add_ego_vehicle()

        self.num_sections.setDisabled(True) #disable changing num_sections after editing sections
        self.vec_populate()
        QtWidgets.QStackedLayout.setCurrentWidget(self.stack,section_vector.page_list[index])
        section_vector.page_list[index].section_id.setCurrentText("Section {}".format(index)) #create edit_section pages and go to selected page
        

    def single_left(self):
        """
        connected to: self.left_arrow
        function: performs a map transition of value = 1 in the left direction
        ex: if road_array = [3,4,5,6,7] --> single_left(road_array) = [2,3,4,5,6]
        """

        if self.road_array[0] == "-" or self.road_array[0] == 1: #do nothing if already as far left as possible
            return

        self.road_array[0] -= 1
        self.road_array[1] -= 1
        self.road_array[2] -= 1
        self.road_array[3] -= 1
        self.road_array[4] -= 1
        self.road_button_reset()
        


    def single_right(self):
        """
        connected to: self.right_arrow
        function: performs a map transition of value = 1 in the right direction
        ex: if road_array = [3,4,5,6,7] --> single_right(road_array) = [4,5,6,7,8]
        """

        if self.road_array[0] == "-": #if no more sections right: return
            return

        val = self.num_sections.value()
        if self.road_array[-1] == val: #if at max section: return
            return

        self.road_array[0] += 1
        self.road_array[1] += 1
        self.road_array[2] += 1
        self.road_array[3] += 1
        self.road_array[4] += 1
        self.road_button_reset()

    def double_left(self):
        """
        connected to: self.double_arrow_left
        function: performs a map transition to the beginning of the road_array
        ex: if road_array = [3,4,5,6,7] --> double_left(road_array) = [1,2,3,4,5]
        """

        if self.road_array[0] == '-':
            return

        self.road_array[0] = 1
        self.road_array[1] = 2
        self.road_array[2] = 3
        self.road_array[3] = 4
        self.road_array[4] = 5
        self.road_button_reset()


    def double_right(self):
        """
        connected to: self.double_arrow_right
        function: performs a map transition to the end of the road_array
        ex: if num_sections = 10 and road_array = [3,4,5,6,7] --> double_right(road_array) = [6,7,8,9,10]
        """

        val = self.num_sections.value()
        if self.road_array[-1] == val:
            return

        j = 4
        for i in range(0,5):
            self.road_array[i] = val - j
            j = j - 1
            if val - j <= 1:
                self.road_array[i] = '-'

        self.road_button_reset()

    
    def back_to_start(self):
        """
        connected to: back_home_pop_up.py-->back_button.clicked
        function: destroys all data in GUI and returns to home.py
        """

        if self.stack.count() > 1:
            for i in range(0,int(self.num_sections.value())):
                self.stack.widget(i).destroy()
        section_vector.page_list.clear()
        self.new = primary.Start_Window()
        self.destroy()
        self.new.show()



    def go_to_general_settings(self):
        """
        connected to: edit_section.py-->back_button.clicked
        function: brings user back to general settings page
        """

        QtWidgets.QStackedLayout.setCurrentWidget(self.stack,section_vector.page_list[0])


    def go_to_page(self, val):
        """
        connected to: edit_section.py-->section_id.changed
        function: brings user to the selected edit_section page when changing the page value in the section_id dropbox
        """

        QtWidgets.QStackedLayout.setCurrentWidget(self.stack,section_vector.page_list[val])
        section_vector.page_list[val].section_id.setCurrentText("Section {}".format(val))

        


    def vec_populate(self):
        """
        connected to: none
        function: used in road_button_click_helper
        populates the page_list found in section_vector.py
        page_list contains all the edit_section pages
        also populates self.stack which contains general settings page and all edit_section pages
        """

        val = self.num_sections.value()

        if val == len(section_vector.page_list)-1: #if section_vector.page_list is already same size as num_sections value, no need to populate page_list
            return

        
        if val > len(section_vector.page_list)-1: #if page list is not yet populated, populate it
            section_vector.populate(section_vector.page_list,val,self) #calls populate function from section_vector
        
            for i in section_vector.page_list: #add all created pages onto stack
                self.stack.addWidget(i)

        #outdated code attempting to allow the changing of num_sections even after simulation is already created
        #leaving this here to assist if this feature is ever developed
        #check README and contact me if you are confused about this function
        """
        if val < len(section_vector.page_list)-1:
            remove_value = len(section_vector.page_list) -1 - val
            i = len(section_vector.page_list)-1
            i_copy = i
            section_vector.remove(section_vector.page_list,remove_value)

            while(remove_value > 0):
                self.stack.removeWidget(self.stack.widget(i))
                i = i - 1
                remove_value = remove_value - 1


            for k in range(1,len(section_vector.page_list)):
                for j in range(len(section_vector.page_list),i_copy):
                    section_vector.page_list[k].section_id.removeItem(j)
        """
        

        
    
    def validate_input_num_sections(self):
        """
        connected to: self.num_sections.changed
        function: whenever edit_sections value is changed, produces the section value on the road_map
        """

        val = self.num_sections.value()

        j = 4
        for i in range(0,5):
            self.road_array[i] = val - j
            j = j - 1
            if val - j <= 1:
                self.road_array[i] = '-'

        self.road_button_reset()
    
        

    
    def validate_input_speed(self):
        """
        connected to: max_speed.inputChanged
                      min_speed.inputChanged
                      max_speed.valueChanged
                      min_speed.valueChanged
        function: does not allow min speed to be greater than max speed or max speed to be lesser than min speed
        """

        upper_bound = self.max_speed.value()
        lower_bound = self.min_speed.value()
        self.min_speed.setMaximum(upper_bound)
        self.max_speed.setMinimum(lower_bound)




    def copy_map_to_sections(self):
        """
        connected to: add_vehicles.py-->back_button.clicked
        function: copies all vehicle information from add_vehicles.py map to every map in each edit_section.py page
        this function allows edit_section.py map to appear to be the same map as add_vehicles.py map at all times
        """

        #find difference in number of cars in add_vehicle page and each edit_section page
        #if there are no new cars, return
        add_vehicles_car_count = len(self.add_vehicles_widget.all_vehicles_list)
        section_vehicles_car_count = len(section_vector.page_list[1].vehicle_list)
        if add_vehicles_car_count == section_vehicles_car_count:
            return


        #for however many new cars there are, copy all of their attributes and put them into
        #a tuple containing all necessary information
        car_attribute_list = list()
        for i in range(section_vehicles_car_count,add_vehicles_car_count):
            car = self.add_vehicles_widget.all_vehicles_list[i]
            lane = car.lane
            lead = car.lead
            gap = car.gap
            model = car.model
            r = car.color_r
            g = car.color_g
            b = car.color_b
            position = car.position
            tupl = tuple((lane,lead,gap,model,r,g,b,position))
            car_attribute_list.append(tupl)

        #iterate over all section pages
        for i in range(1,len(section_vector.page_list)):
            edit_page = section_vector.page_list[i] #current page to add vehicles to
            z = section_vehicles_car_count + 1 #vehicle number that will appear on new vehicles added (indexed starting at 1)

            for settings in car_attribute_list: #iterate over new vehicle settings
                car_copy = vehicle.Vehicle(settings[0],settings[1],settings[2],settings[3],settings[4],settings[5],settings[6])
                car_copy.position = settings[7]
                car_copy.setParent(edit_page.map_background)

                self.left_follow_gaps = self.add_vehicles_widget.left_follow_gaps #all gap values as stored in add_vehicles page to help car placement
                self.subject_follow_gaps = self.add_vehicles_widget.subject_follow_gaps
                self.left_lead_gaps = self.add_vehicles_widget.left_lead_gaps
                self.subject_lead_gaps = self.add_vehicles_widget.subject_lead_gaps

                placement_reference = section_vector.page_list[i].map_background.width() #place cars relative to map width

                if car_copy.lead == 0:
                    if car_copy.lane == "subject":
                        car_copy.move(placement_reference/1.48, self.subject_lead_gaps[edit_page.subject_lead_count])
                        edit_page.subject_lead_count += 1
                    else:
                        car_copy.move(placement_reference/1.77, self.left_lead_gaps[edit_page.left_lead_count])
                        edit_page.left_lead_count += 1

                else:
                    if car_copy.lane == "subject":
                        car_copy.move(placement_reference/1.48, self.subject_follow_gaps[edit_page.subject_follow_count])
                        edit_page.subject_follow_count += 1
                    else:
                        car_copy.move(placement_reference/1.77, self.left_follow_gaps[edit_page.left_follow_count])
                        edit_page.left_follow_count += 1
                
                #use z-1 to edit pages because z indexing starts at 1
                #changes edit_vehicle pages for each vehicle to proper rgb and model values
                section_vector.page_list[i].edit_vehicle_list[z-1].title_text.setText("Edit Vehicle {}".format(z))
                section_vector.page_list[i].edit_vehicle_list[z-1].car_index = z -1
                section_vector.page_list[i].edit_vehicle_list[z-1].vehicle_model.setCurrentText(settings[3])
                section_vector.page_list[i].edit_vehicle_list[z-1].vehicle_color_r.setValue(settings[4])
                section_vector.page_list[i].edit_vehicle_list[z-1].vehicle_color_g.setValue(settings[5])
                section_vector.page_list[i].edit_vehicle_list[z-1].vehicle_color_b.setValue(settings[6])
                
                #use z-1 to connect car click to function car_click()
                #set object name for convenience
                #set text of vehicle to z value, increment z by 1
                car_copy.clicked.connect(partial(self.car_click,i,z-1) ) #each car is clickable to open up its edit_vehicle page    
                car_copy.setObjectName("car")
                car_copy.setText(str(z))
                section_vector.page_list[i].vehicle_list.append(car_copy)
                z+=1
                car_copy.show()



    def add_vehicle_edit_windows(self):
        """
        connected to: add_vehicles.py-->back_button.clicked
        function: For any new vehicles added in add_vehicle.py, this function will create an edit_vehicle.py page for it
        and place it within edit_section.py to make the vehicle editable
        """

        #find current number of vehicles in add_vehicles.py and current number of edit_vehicle pages in each edit_section page
        #the difference between these numbers is how many new edit_vehicle pages we will need to create
        car_count = len(self.add_vehicles_widget.all_vehicles_list)
        page_count = len(section_vector.page_list[1].edit_vehicle_list)


        for page in range(1,len(section_vector.page_list)): #for each edit_section.py page
            for car_index in range(page_count,car_count): #for each new vehicle added in add_vehicles.py
                edit_car = edit_vehicle.Edit_Vehicle_Widget(car_index+1,section_vector.page_list[page])
                edit_car.setParent(section_vector.page_list[page])
                edit_car.setObjectName("edit") #set object name for later reference
                edit_car.safety_distance.setValue(self.safety_distance.value()) 
                edit_car.hide()
                section_vector.page_list[page].edit_vehicle_list.append(edit_car) #add edit page to edit_vehicle_list for later reference



    def car_click(self,page_index,car_index):
        """
        connected to: edit_section.py-->car.clicked
        function: This function is called whenever a car object is clicked on. It will display the vehicle's own edit_vehicle.py page
        """

        section_vector.page_list[page_index].edit_vehicle_list[car_index].show()
        section_vector.page_list[page_index].edit_vehicle_list[car_index].raise_()


    #you may delete this function -- it is just for reference and has no actual use
    def gather(self):
        """
        connected to: None
        function: This is just for reference. This function shows how to retrieve all the data from different pages throughout the simulation.
        This will be a helpful reference if you are new to using PYQT5
        """

        #general setings
        number_freeway_sections = self.num_sections.value()
        allow_collisions = self.allow_collisions.isChecked()
        minimum_speed = self.min_speed.value()
        max_speed = self.max_speed.value()
        safety_distance = self.safety_distance.value()

        print("---SETUP INFO---")
        print("number of sections:",number_freeway_sections)
        print("allow collisions (t/f):",allow_collisions)
        print("minimum speed:",minimum_speed)
        print("maximum speed:",max_speed)
        print("safety distance:",safety_distance,"\n")



        #left lane car info in tuple form (gap,model,lead(t/f),red,green,blue)
        left_cars = list()
        for i in self.add_vehicles_widget.left_vehicle_list:
            data = tuple((i.gap,i.model,i.lead,i.color_r,i.color_g,i.color_b))
            left_cars.append(data)

        #right lane car info in tuple form (gap,model,lead(t/f),red,green,blue)
        subject_cars = list()
        for i in self.add_vehicles_widget.subject_vehicle_list:
            data = tuple((i.gap,i.model,i.lead,i.color_r,i.color_g,i.color_b))
            subject_cars.append(data)

                

        print("---LEFT LANE INFO---")
        for index,car in enumerate(left_cars):
            print("Vehicle {}:".format(index+1))
            print("Color: ({},{},{})".format(car[3],car[4],car[5]))
            print("Gap:",car[0])
            print("Model:",car[1])
            print("Lead:",car[2],"\n")

        print("---SUBJECT LANE INFO---")
        for index,car in enumerate(subject_cars):
            print("Vehicle {}:".format(index+1))
            print("Color: ({},{},{})".format(car[3],car[4],car[5]))
            print("Gap:",car[0])
            print("Model:",car[1])
            print("Lead:",car[2],"\n")


        print("---EGO VEHICLE SETTINGS---")
        ego = self.edit_ego_vehicle
        print("Model:", ego.vehicle_model.currentText())
        print("Color: ({},{},{})".format(ego.vehicle_color_r.toPlainText(),ego.vehicle_color_g.toPlainText(),ego.vehicle_color_b.toPlainText()))
        print("Safety distance:", ego.safety_distance.toPlainText())
        print("\n")


        print("---VEHICLE BEHAVIOR INFO---")
        for i in range(1,len(section_vector.page_list)):
            print("\n--Section {}--".format(i))
            for j in section_vector.page_list[i].edit_vehicle_list:
                print("-Vehicle {}-".format(j.car_index + 1))
                print("Vary Speed:", j.vary_speed_button.isChecked())
                print("Maintain Speed:", j.maintain_speed_button.isChecked())
                print("Lane Change:", j.lane_change_yes.isChecked())
                if j.lane_change_yes.isChecked():
                    print("Lane Change Time:", j.lane_change_time.toPlainText())
                print("Safety Distance:", j.safety_distance.toPlainText())
                if j.vehicle_color_r.toPlainText() == "":
                    print("Color: Default")
                else:
                    print("Color: ({},{},{})".format(j.vehicle_color_r.toPlainText(),j.vehicle_color_g.toPlainText(),j.vehicle_color_b.toPlainText()))



    def run(self):

        #gather general settings
        num_vehicles = len(self.add_vehicles_widget.all_vehicles_list)
        allow_collisions = self.allow_collisions.isChecked()
        minimum_speed = self.min_speed.value()
        maximum_speed = self.max_speed.value()
        view = self.start_sim_pop_up.choose_view.currentIndex()
        control = self.start_sim_pop_up.choose_control.currentIndex()

        try:
            #set environment min and max speeds
            self.freewayenv.max_speed = maximum_speed
            self.freewayenv.min_speed = minimum_speed

            #vehicle behavior settings
            for i in range(1,len(section_vector.page_list)):
                for j in range(0,num_vehicles):
                    car_index = section_vector.page_list[i].edit_vehicle_list[j].car_index #select current vehicle to pull information from

                    current_car = None
                    for cars in self.add_vehicles_widget.all_vehicles_list: #find which vehicle to pull driving settings from
                        if str(car_index + 1) == cars.text():
                            current_car = cars

                    #retrieve all inputted data from edit_vehicle.py
                    lane_input = current_car.lane
                    position_input = current_car.position
                    command_input1 = "speed"
                    command_input1_time = 0
                    command_input2 = "speed"
                    lead_input = "lead"

                    #lead/follow
                    if current_car.lead == 1:
                        lead_input = "follow"  

                    #lane change yes/no
                    if section_vector.page_list[i].edit_vehicle_list[j].lane_change_yes.isChecked():
                        command_input1 = "lane"
                        command_input1_time = section_vector.page_list[i].edit_vehicle_list[j].lane_change_time.value()
                    
                    #vary speed/maintain distance
                    if section_vector.page_list[i].edit_vehicle_list[j].vary_speed_button.isChecked():
                        command_input2 = "distance"
                    
                    #currently the backend only supports a single command applied to each vehicle in the simulation
                    #if the ability to apply two commands is implemented, uncomment this line to allow for the "distance" command
                    #self.freewayenv.edit_normal_section_setting(i,lead_input,lane_input,position_input,command=command_input2)
                    
                    #set vehicle behavior settings 
                    self.freewayenv.edit_normal_section_setting(i,lead_input,lane_input,position_input,command=command_input1,command_start_time=command_input1_time)


            #view choice
            if view == 0:
                spec_mode = "human_driving"
            elif view == 1:
                spec_mode = "first_person"
            else:
                spec_mode = None

            #control choice
            if control == 0:
                control_mode = False
            else:
                control_mode = True

            #begin simulation
            self.freewayenv.SectionBackend(spectator_mode=spec_mode,allow_collision=allow_collisions,enable_human_control=control_mode)

        finally:
            time.sleep(5)
            self.env.destroy_actors()
            
            
    def initUI(self):
        """
        Initializes all the UI componenets on the Freeway Window.
        
        Runs when the Freeway Window is created. Creates all of the UI 
        components that enable to user to interact and design an experiment.
        """
        #CARLA SETTINGS
        self.stack = QStackedLayout() #stack contains freeway_window.py and all edit_section.py pages
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.stack)
        self.setCentralWidget(self.main_widget) #central widget necessary for pyqt5 to function correctly

        self.general_settings_widget = QWidget()
        self.grid = QGridLayout()
        self.general_settings_widget.setLayout(self.grid)
        self.stack.addWidget(self.general_settings_widget)
        section_vector.page_list.append(self.general_settings_widget) #adds freeway_window to page list
        
        #CONNECTED PAGES/WIDGETS

            #add vehicles widget
            #to edit, see add_vehicles.py
        self.add_vehicles_widget = add_vehicles.Add_Vehicles_Window(self,self)
        self.add_vehicles_widget.hide()


            #edit ego vehicle widget
            #to edit, see edit_vehicle_ego.py
        self.edit_ego_vehicle = edit_vehicle_ego.Edit_Vehicle_Ego_Widget(self)
        self.edit_ego_vehicle.hide()


            #start sim pop up widget
            #to edit, see start_sim_pop_up.py
        self.start_sim_pop_up = start_sim_pop_up.Start_Sim_Pop_Up(self)
        self.start_sim_pop_up.move(primary.width/2.3,primary.height/2.3)
        self.start_sim_pop_up.hide()


            #back button pop up widget
            #to edit, see back_home_pop_up.py
        self.back_button_pop_up = back_home_pop_up.Back_Home_Pop_Up(self)
        self.back_button_pop_up.move(primary.width/2.3,primary.height/2.3)
        self.back_button_pop_up.hide()


        #PAGE DATA (for functions below)

            #carla_vehicle_list
        self.carla_vehicle_list_subject_lead = list()
        self.carla_vehicle_list_subject_follow = list()
        self.carla_vehicle_list_left_lead = list()
        self.carla_vehicle_list_left_follow = list()

        #back button
        self.back_button = QPushButton()
        self.back_button.setText("Back to Start")
        self.back_button.setFont(QFont("Arial", 18))
        self.back_button.setMaximumWidth(primary.width/10)
        self.back_button.setMaximumHeight(primary.height/26)
        self.back_button.clicked.connect(self.back_button_pop_up.show)
        
        #General Settings text
        self.general_settings = QLabel()
        self.general_settings.setText("General Settings")
        self.general_settings.setFont(QFont("Arial", 24))
        self.general_settings.setAlignment(QtCore.Qt.AlignCenter)
        self.general_settings.setMaximumHeight(primary.height/10)
        
        #Allow Collisions
        self.allow_collisions_text = QLabel()
        self.allow_collisions_text.setText("Allow Collisions")
        self.allow_collisions_text.setFont(QFont("Arial", 18))

        self.allow_collisions = QCheckBox()
        self.allow_collisions.setChecked(True)
        size_val = str(primary.height/20) 
        self.allow_collisions.setStyleSheet("QCheckBox::indicator { width: %spx; height: %spx;}" % (size_val,size_val))

        #Number of Freeway Sections
        self.num_sections_text = QLabel()
        self.num_sections_text.setText("Number of Freeway Sections")
        self.num_sections_text.setFont(QFont("Arial", 18))
        self.num_sections_text.setMinimumWidth(primary.width/4) #controls dist between input boxes and input text

        self.num_sections = QSpinBox()
        self.num_sections.setMaximumHeight(primary.height/20)
        self.num_sections.setMaximumWidth(primary.height/20)
        self.num_sections.setMinimumHeight(primary.height/20)
        self.num_sections.setMinimumWidth(primary.height/20)
        self.num_sections.setValue(0)
        self.num_sections.setMinimum(1)
        self.num_sections.setMaximum(7)
        self.num_sections.valueChanged.connect(self.validate_input_num_sections)


        #Min Speed
        self.min_speed_text = QLabel()
        self.min_speed_text.setText("Minimum Speed (m/s)")
        self.min_speed_text.setFont(QFont("Arial", 18))

        self.min_speed = QSpinBox()
        self.min_speed.setMaximumHeight(primary.height/20)
        self.min_speed.setMaximumWidth(primary.height/20)
        self.min_speed.setMinimumHeight(primary.height/20)
        self.min_speed.setMinimumWidth(primary.height/20)
        self.min_speed.setMinimum(0)
        self.min_speed.setValue(15)
        self.min_speed.valueChanged.connect(self.validate_input_speed)
        self.min_speed.textChanged.connect(self.validate_input_speed)


        #Max Speed
        self.max_speed_text = QLabel()
        self.max_speed_text.setText("Maximum Speed (m/s)")
        self.max_speed_text.setFont(QFont("Arial", 18))

        self.max_speed = QSpinBox()
        self.max_speed.setMaximumHeight(primary.height/20)
        self.max_speed.setMaximumWidth(primary.height/20)
        self.max_speed.setMinimumHeight(primary.height/20)
        self.max_speed.setMinimumWidth(primary.height/20)
        self.max_speed.setMinimum(self.min_speed.value())
        self.max_speed.setMaximum(150)
        self.max_speed.setValue(30)
        self.max_speed.valueChanged.connect(self.validate_input_speed)
        self.max_speed.textChanged.connect(self.validate_input_speed)
        self.min_speed.setMaximum(self.max_speed.value())


        #Safety Distance
        self.safety_distance_text = QLabel()
        self.safety_distance_text.setText("Safety Distance (m)")
        self.safety_distance_text.setFont(QFont("Arial", 18))

        self.safety_distance = QSpinBox()
        self.safety_distance.setMaximumHeight(primary.height/20)
        self.safety_distance.setMaximumWidth(primary.height/20)
        self.safety_distance.setMinimumHeight(primary.height/20)
        self.safety_distance.setMinimumWidth(primary.height/20)
        self.safety_distance.setValue(15)
        self.safety_distance.setMinimum(5)
        self.safety_distance.setMaximum(999)

        #Start Simulation
        self.start_simulation = QPushButton()
        self.start_simulation.setText("Start Simulation")
        self.start_simulation.setFont(QFont("Arial", 14))
        self.start_simulation.setMaximumWidth(primary.width/6)
        self.start_simulation.setMinimumHeight(primary.height/25)
        self.start_simulation.clicked.connect(self.start_sim_pop_up.show)

        #MAP SETTINGS

            #widget
        self.map_widget = QWidget()
        self.map_widget.setMinimumWidth(primary.width/2.03)
        self.map_widget.setMinimumHeight(primary.height/2.1)

            #background color
        self.map_background = QLabel(self.map_widget)
        self.map_background.setStyleSheet("background-color: #cccac6;")
        self.map_background.setMinimumHeight(primary.height/2.15)
        self.map_background.setMinimumWidth(primary.width/2.75)

            #map
        self.pixmap = QPixmap('images/road.gif')
        self.pixmap = self.pixmap.scaledToHeight(primary.height/2.5)

        self.map1 = QLabel(self.map_widget)
        self.map1.setPixmap(self.pixmap)
        self.map2 = QLabel(self.map_widget)
        self.map2.setPixmap(self.pixmap)
        self.map3 = QLabel(self.map_widget)
        self.map3.setPixmap(self.pixmap)
        self.map4 = QLabel(self.map_widget)
        self.map4.setPixmap(self.pixmap)
        self.map5 = QLabel(self.map_widget)
        self.map5.setPixmap(self.pixmap)

            #arrow pixmap objects
        self.arrow_pixmap = QPixmap('images/next.png')
        self.arrow_pixmap = self.arrow_pixmap.scaledToHeight(primary.height/12)
        self.arrow_pixmap_left = self.arrow_pixmap.transformed(QtGui.QTransform().scale(-1,1))
        self.double_arrow_pixmap = QPixmap('images/double_next.png')
        self.double_arrow_pixmap = self.double_arrow_pixmap.scaledToHeight(primary.height/12)
        self.double_arrow_pixmap_left = self.double_arrow_pixmap.transformed(QtGui.QTransform().scale(-1,1))

            #arrows
        self.right_arrow = ExtendedQLabel(self.map_widget)
        self.right_arrow.setPixmap(self.arrow_pixmap)
        self.right_arrow.clicked.connect(self.single_right)

        self.double_arrow_right = ExtendedQLabel(self.map_widget)
        self.double_arrow_right.setPixmap(self.double_arrow_pixmap)
        self.double_arrow_right.clicked.connect(self.double_right)

        self.left_arrow = ExtendedQLabel(self.map_widget)
        self.left_arrow.setPixmap(self.arrow_pixmap_left)
        self.left_arrow.clicked.connect(self.single_left)

        self.double_arrow_left = ExtendedQLabel(self.map_widget)
        self.double_arrow_left.setPixmap(self.double_arrow_pixmap_left)
        self.double_arrow_left.clicked.connect(self.double_left)

            #clickable buttons on road sections
        self.road_array = ["-","-","-","-","1"]

        self.road_button1 = QPushButton(self.map_widget)
        self.road_button1.setMaximumWidth(primary.width/30)
        self.road_button1.setMinimumWidth(primary.width/30)
        self.road_button1.setMaximumHeight(primary.height/25)
        self.road_button1.setMinimumHeight(primary.height/25)
        self.road_button1.setText(str(self.road_array[0]))
        self.road_button1.clicked.connect(lambda: self.road_button_click_helper(self.road_button1.text()))

        self.road_button2 = QPushButton(self.map_widget)
        self.road_button2.setMaximumWidth(primary.width/30)
        self.road_button2.setMinimumWidth(primary.width/30)
        self.road_button2.setMaximumHeight(primary.height/25)
        self.road_button2.setMinimumHeight(primary.height/25)
        self.road_button2.setText(str(self.road_array[1]))
        self.road_button2.clicked.connect(lambda: self.road_button_click_helper(self.road_button2.text()))

        self.road_button3 = QPushButton(self.map_widget)
        self.road_button3.setMaximumWidth(primary.width/30)
        self.road_button3.setMinimumWidth(primary.width/30)
        self.road_button3.setMaximumHeight(primary.height/25)
        self.road_button3.setMinimumHeight(primary.height/25)
        self.road_button3.setText(str(self.road_array[2]))
        self.road_button3.clicked.connect(lambda: self.road_button_click_helper(self.road_button3.text()))

        self.road_button4 = QPushButton(self.map_widget)
        self.road_button4.setMaximumWidth(primary.width/30)
        self.road_button4.setMinimumWidth(primary.width/30)
        self.road_button4.setMaximumHeight(primary.height/25)
        self.road_button4.setMinimumHeight(primary.height/25)
        self.road_button4.setText(str(self.road_array[3]))
        self.road_button4.clicked.connect(lambda: self.road_button_click_helper(self.road_button4.text()))

        self.road_button5 = QPushButton(self.map_widget)
        self.road_button5.setMaximumWidth(primary.width/30)
        self.road_button5.setMinimumWidth(primary.width/30)
        self.road_button5.setMaximumHeight(primary.height/25)
        self.road_button5.setMinimumHeight(primary.height/25)
        self.road_button5.setText(str(self.road_array[4]))
        self.road_button5.clicked.connect(lambda: self.road_button_click_helper(self.road_button5.text()))

        #GRID SETTINGS

            #labels and text
        self.grid.addWidget(self.back_button,          0,0,1,1)
        self.grid.addWidget(self.general_settings,     1,0,1,1)
        self.grid.addWidget(self.allow_collisions_text,2,0,1,1)
        self.grid.addWidget(self.num_sections_text,    3,0,1,1)
        self.grid.addWidget(self.max_speed_text,       4,0,1,1)
        self.grid.addWidget(self.min_speed_text,       5,0,1,1)
        self.grid.addWidget(self.safety_distance_text, 6,0,1,1)
        self.grid.addWidget(self.start_simulation,     7,0,1,1)

            #input boxes
        self.grid.addWidget(self.allow_collisions,     2,1,1,1)
        self.grid.addWidget(self.num_sections,         3,1,1,1)
        self.grid.addWidget(self.max_speed,            4,1,1,1)
        self.grid.addWidget(self.min_speed,            5,1,1,1)
        self.grid.addWidget(self.safety_distance,      6,1,1,1)
    

            #map
        move_dist = (primary.width/12)
        self.grid.addWidget(self.map_widget,          2,2,-1,-1)
        self.map_background.move(primary.width/12,0)
        self.map1.move(move_dist*1.2,primary.height/40)
        self.map2.move(move_dist*2.0,primary.height/40)
        self.map3.move(move_dist*2.8,primary.height/40)
        self.map4.move(move_dist*3.6,primary.height/40)
        self.map5.move(move_dist*4.4,primary.height/40)

            #arrows
        self.right_arrow.move(primary.width/2.37,primary.height/6)
        self.left_arrow.move(primary.width/17.37, primary.height/6)
        self.double_arrow_right.move(primary.width/2.18,primary.height/6)
        self.double_arrow_left.move(primary.width/26.37, primary.height/6)


            #road buttons
        self.road_button1.move(primary.width/8.7,primary.height/5.1)
        self.road_button2.move(primary.width/5.55,primary.height/5.1)
        self.road_button3.move(primary.width/4.05,primary.height/5.1)
        self.road_button4.move(primary.width/3.18,primary.height/5.1)
        self.road_button5.move(primary.width/2.62,primary.height/5.1)
    

def main():
    primary.main()

if __name__ == "__main__":
    main()
