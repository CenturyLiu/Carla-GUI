#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Weixin Feng
"""

import sys
sys.path.append("..")
sys.path.append("E:\WindowsNoEditor\PythonAPI\example\gui intersection")
sys.path.append("E:\WindowsNoEditor\PythonAPI\example\backend")
sys.path.append("E:\WindowsNoEditor\PythonAPI\example")
sys.path.append("E:\WindowsNoEditor\PythonAPI\carla\dist\carla-0.9.9-py3.7-win-amd64.egg")

import glob
from configobj import ConfigObj
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
import intersection
import carla
from backend.intersection_settings_helper import write_intersection_settings, read_intersection_settings
from backend.carla_env import CARLA_ENV # self-written class that provides help functions
from backend.multiple_vehicle_control import VehicleControl
from backend.initial_intersection import  create_intersections, get_ego_spectator, get_ego_left_spectator
from backend.full_path_vehicle import LeadVehicleControl, FollowVehicleControl
from backend.intersection_definition import get_traffic_lights
from backend.intersection_definition import Intersection
from backend.intersection_backend import IntersectionBackend

widgetmaps = []
world_pos_list = [(-190.0,0.0),(-133.0,0.0),(-55.0,0.0),(25.4,0.0)]

#helper function, get label text
def ExtractText(label):
    temp = QTextEdit()
    temp.setText(label.text())
    text = temp.toPlainText()
    del temp
    return text

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # variables needed for intersections
        self.light_list_all = []      
        self.car_list = []
        self.delete_car = []
        self.saved_intersections = []
        self.cur_inter = 0
        self.cur_light = 0
        self.cur_lane = 0
        self.redLightDuration = 10
        self.yellowLightDuration = 5
        self.greenLightDuration = 10
        self.gloSafetyDistance = 15
        self.ego_spawned = False
        self.cur_ID = [0, 0, 0]
        self.normal_num = -1
        self.penetrate_dis = 0



        ### Front end setup ###
        #variables create
        self.collision = True
        self.navigation_speed = 10.0
        self.safety_distance = 15
        self.ego = -1
        self.lead = -1
        self.follow = -1
        
        
        # build ui
        self.inter = intersection.Ui_Form()
        self.inter.setupUi()
        self.inter.showMaximized()
        self.TrafLit = intersection.Ui_TrafLightSet()
        self.TrafLit.setupUi()
        self.addVeh = intersection.Ui_AddVehicle()
        self.addVeh.setupUi()
        self.errMes = intersection.Ui_ErrMes()
        self.errMes.setupUi()
        self.simulation = intersection.Ui_Simulation()
        self.simulation.setupUi()
        self.pene = intersection.Ui_Penetrate()
        self.pene.setupUi()

        #add 6 widget maps in list
        widgetmaps.append(self.inter.widget3Fro)
        widgetmaps.append(self.inter.widget4Fro)
        widgetmaps.append(self.inter.widget5Fro)
        widgetmaps.append(self.inter.widget6Fro)
        widgetmaps.append(self.inter.widget7Fro)
        widgetmaps.append(self.inter.widget8Fro)

        #link buttons and input
        self.inter.RightFro.clicked.connect(self.right)
        self.inter.LeftFro.clicked.connect(self.left)
        self.inter.RightMostFro.clicked.connect(self.rightMost)
        self.inter.LeftMostFro.clicked.connect(self.leftMost)
        self.inter.spinBoxNumIntFro.valueChanged.connect(self.change_int)
        self.inter.Int1Fro.clicked.connect(lambda: self.front_inter(num = 1))
        self.inter.Int2Fro.clicked.connect(lambda: self.front_inter(num = 2))
        self.inter.Int3Fro.clicked.connect(lambda: self.front_inter(num = 3))
        self.inter.Int4Fro.clicked.connect(lambda: self.front_inter(num = 4))
        self.inter.Int5Fro.clicked.connect(lambda: self.front_inter(num = 5))
        self.inter.Int6Fro.clicked.connect(lambda: self.front_inter(num = 6))
        self.inter.checkBoxColFro.stateChanged.connect(self.collision_change)
        self.inter.spinBoxMaxVFro.valueChanged.connect(self.Max_speed_set)
        self.inter.spinBoxSafDisFro.valueChanged.connect(self.safety_distance_set)
        self.inter.backButtonInt.clicked.connect(self.inter_front)
        self.inter.TrafLightInt.clicked.connect(self.inter_Light)
        self.inter.backButtonLit.clicked.connect(self.Light_inter)
        self.inter.backButtonSpa.clicked.connect(self.spawn_inter)
        self.inter.AddVehInt.clicked.connect(self.inter_spawn)
        self.inter.set1Lit.clicked.connect(lambda: self.OpenTrafLit(num = 0))
        self.inter.set2Lit.clicked.connect(lambda: self.OpenTrafLit(num = 1))
        self.inter.set3Lit.clicked.connect(lambda: self.OpenTrafLit(num = 2))
        self.inter.set4Lit.clicked.connect(lambda: self.OpenTrafLit(num = 3))
        self.inter.AddSubSpa.clicked.connect(lambda: self.OpenAddVeh(num = 0))
        self.inter.AddLeftSpa.clicked.connect(lambda: self.OpenAddVeh(num = 1))
        self.inter.AddAheadSpa.clicked.connect(lambda: self.OpenAddVeh(num = 2))
        self.inter.AddRightSpa.clicked.connect(lambda: self.OpenAddVeh(num = 3))
        self.inter.confirmVeh.clicked.connect(self.confirm)
        self.inter.cobBoxIDInt.currentIndexChanged.connect(self.change_inter)
        self.inter.cobBoxImportInt.currentIndexChanged.connect(self.import_inter)
        self.inter.StartSimFro.clicked.connect(self.Front_simulation)
        self.inter.DeleteVeh.clicked.connect(self.deleteCar)
        self.inter.cobBoxStopVeh.currentIndexChanged.connect(self.Veh_penetrate)

        for i in range(4):
            name = "CarSub" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.clicked.connect(self.make_any_vehicle(x = 0, y = i))

        for i in range(4):
            name = "CarLeft" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.clicked.connect(self.make_any_vehicle(x = 1, y = i))

        for i in range(4):
            name = "CarAhead" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.clicked.connect(self.make_any_vehicle(x = 2, y = i))
        
        for i in range(4):
            name = "CarRight" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.clicked.connect(self.make_any_vehicle(x = 3, y = i))



        self.inter.backButtonVeh.clicked.connect(self.vehicle_inter)
        self.TrafLit.buttonBoxTLDia.accepted.connect(self.traffic_light_ok)
        self.addVeh.buttonBoxAdDia.accepted.connect(self.add_vehicle_ok)
        self.simulation.buttonBoxSimDia.accepted.connect(self.start_simulation)

        ### back end setup ###
        self.client = carla.Client("localhost",2000)
        self.client.set_timeout(20.0)
        self.world = self.client.load_world('Town05')
        self.spectator = self.world.get_spectator()
        self.spectator.set_transform(carla.Transform(carla.Location(x=-190, y=1.29, z=75.0), carla.Rotation(pitch=-88.0, yaw= -1.85, roll=1.595)))
        self.env = CARLA_ENV(self.world)  
        self.traffic_light_list = get_traffic_lights(self.world.get_actors())
        self.intersection_list = create_intersections(self.env, 6, self.traffic_light_list, self.navigation_speed)
        




        #lists initialized
        for i in range(6): # changed all to 6 was 4
            light_list_one = [[0.00, 10.00, 10.00, 15.00, 15.00, 25.00], [0.00, 10.00, 10.00, 15.00, 15.00, 25.00], [0.00, 10.00, 10.00, 15.00, 15.00, 25.00], [0.00, 10.00, 10.00, 15.00, 15.00, 25.00]]
            self.light_list_all.append(light_list_one)
            self.saved_intersections.append(None)
            inter_list = []
            for j in range(6):
                lane_list = []
                inter_list.append(lane_list)

            self.car_list.append(inter_list)
        for i in range(6):
            inter_list = []
            for j in range(6):
                lane_list = []
                for k in range(6):
                    lane_list.append(False)
                inter_list.append(lane_list)
            self.delete_car.append(inter_list)

        self.spawn_ego_default()
        self.show_win()

       

    def spawn_ego_default(self):
        #add ego 
        index = self.addVeh.cobBoxModAdDia.currentIndex()
        gapNum = self.addVeh.spinBoxGapAdDia.value()
        model_combine = self.addVeh.model_list[index].split()
        model1 = model_combine[0]
        model2 = model_combine[1]
        Mname = "vehicle." + model1 + "." + model2
        R = "255"
        G = "255"
        B = "255"

        color = R + "," + G + "," + B
        self.cur_inter = 0
        self.cur_lane = 0
        car2 = self.intersection_list[self.cur_inter].add_ego_vehicle(gap=gapNum, model_name=Mname, safety_distance=self.gloSafetyDistance, vehicle_color=color)                
        car1 = self.intersection_list[self.cur_inter].add_lead_vehicle(lead_distance= 10, vehicle_color="255,255,255", safety_distance=self.gloSafetyDistance)
        car3 = self.intersection_list[self.cur_inter].add_follow_vehicle(follow_distance= 10, vehicle_color="255,255,255", safety_distance=self.gloSafetyDistance)
         
        #put into car list for further use
        self.car_list[self.cur_inter][self.cur_lane].append(car1)
        self.car_list[self.cur_inter][self.cur_lane].append(car2)
        self.car_list[self.cur_inter][self.cur_lane].append(car3)
        self.normal_num = 3
        
        self.ego_spawned = True
        self.show_car()

    #front end haddle change of intersection
    def show_win(self):
        if len(self.intersection_list) > 6:
            #show all buttons if number intersections more than 6 
            self.inter.spacerItemFro1.changeSize(406, 200, QtWidgets.QSizePolicy.MinimumExpanding)            
            self.inter.RightFro.show()
            self.inter.RightMostFro.show()
            self.inter.LeftFro.show()
            self.inter.LeftMostFro.show()
            for i in range(6):
                Button = widgetmaps[i].findChild(QPushButton)
                Button.show()

            #hide left or right arrow if reached end
            if ExtractText(self.inter.Int1Fro) == "1":
                self.inter.spacerItemFro1.changeSize(500, 200, QtWidgets.QSizePolicy.MinimumExpanding)                
                self.inter.LeftFro.hide()
                self.inter.LeftMostFro.hide()
            if ExtractText(self.inter.Int6Fro) == str(len(self.intersection_list)):
                self.inter.RightFro.hide()
                self.inter.RightMostFro.hide()
        else:
            #hide arrows if intersection less than 6
            self.inter.spacerItemFro1.changeSize(500, 200, QtWidgets.QSizePolicy.MinimumExpanding)
            self.inter.RightFro.hide()
            self.inter.RightMostFro.hide()
            self.inter.LeftFro.hide()
            self.inter.LeftMostFro.hide()
            print("length of intersection",len(self.intersection_list))
            for i in range(len(self.intersection_list)):
                Button = widgetmaps[i].findChild(QPushButton)
                Button.show()
            """
            for i in range(len(self.intersection_list), 6):
                Button = widgetmaps[i].findChild(QPushButton)
                Button.hide()
            """


    # back end haddle change of intersection
    def change_int(self):
        
        num = self.inter.spinBoxNumIntFro.value()

        # attempt to support 6 intersection, 4 must work
        num = min(num, 6)
        self.inter.spinBoxNumIntFro.setValue(num)

        IntNFro = [self.inter.Int1Fro, self.inter.Int2Fro, self.inter.Int3Fro, 
                   self.inter.Int4Fro, self.inter.Int5Fro, self.inter.Int6Fro,]
        # it is much easier to stop user from click the button
        for i in range(num, 6):
            IntNFro[i].setEnabled(False)
        for i in range(0, num):
            IntNFro[i].setEnabled(True)

        self.show_win()

    # set up the intersection list based on spinBoxNumIntFro
    def setup_intersection_list(self):
        num = self.inter.spinBoxNumIntFro.value()
        print("final intersection size is", num)
        print("intersection list has length", len(self.intersection_list))
        # default we have intersection_list with length 4
        del self.intersection_list[num:]
        print("intersection list has length", len(self.intersection_list))

    #front page go right
    def right(self):
        for i in self.inter.label_num:
            num = int(ExtractText(i))
            num += 1
            i.setText(str(num))
        self.show_win()
    
    #front page go left
    def left(self):
        for i in self.inter.label_num:
            num = int(ExtractText(i))
            num -= 1
            i.setText(str(num))
        self.show_win()

    #front page go rightmost
    def rightMost(self):
        for i in self.inter.label_num:
            num = len(self.intersection_list) - 5
            num += self.inter.label_num.index(i)
            i.setText(str(num))
        self.show_win()
    
    #front page go leftmost
    def leftMost(self):
        for i in self.inter.label_num:
            num = 1
            num += self.inter.label_num.index(i)
            i.setText(str(num))
        self.show_win()

    #front page go to intersection page
    def front_inter(self, num): 
        self.cur_inter = num - 1
        self.inter.cobBoxIDInt.blockSignals(True)
        self.inter.cobBoxIDInt.setCurrentIndex(num - 1)
        self.inter.cobBoxIDInt.blockSignals(False)
        self.inter.widgetFrontAll.hide()
        self.clean_car()
        self.show_car()        
        self.inter.widgetIntAll.show()

    #intersection page go to front page
    def inter_front(self):
        self.inter.widgetFrontAll.show()
        saved_file = self.intersection_list[self.cur_inter].export_settings()
        self.saved_intersections[self.cur_inter] = saved_file
        index = self.inter.cobBoxImportInt.findText("intersection " + str(self.cur_inter + 1))
        if index == -1:
            self.inter.cobBoxImportInt.addItem("intersection " + str(self.cur_inter + 1))
        self.inter.widgetIntAll.hide()
    
    #intersection page go to trafic light page
    def inter_Light(self):
        self.inter.widgetInt.hide()
        self.inter.widgetLit.show()

    #trafic light page go to intersection page
    def Light_inter(self):
        self.inter.widgetInt.show()
        self.inter.widgetLit.hide()
    
    #intersection page go to spawn page
    def inter_spawn(self):
        self.inter.widgetInt.hide()
        self.inter.widgetSpa.show()

    #spawn page go to intersection page
    def spawn_inter(self):
        self.inter.widgetInt.show()
        self.inter.widgetSpa.hide()

    # function maker for any page to vehicle page
    def make_any_vehicle(self, x, y):
        def any_vehicle():
            #preset settings for car
            uniqueName = self.car_list[self.cur_inter][x][y]
            self.cur_ID[0] = uniqueName
            self.cur_ID[1] = x
            self.cur_lane = x
            self.cur_ID[2] = y
            settings = self.intersection_list[self.cur_inter].get_vehicle_settings(uniqueName)
            
            gap = settings["gap"]
            self.inter.spinBoxGapVeh.setValue(gap)
            
            command = settings["command"]
            if command == "straight":
                self.inter.cobBoxTurnVeh.setCurrentIndex(0)
            elif command == "left":
                self.inter.cobBoxTurnVeh.setCurrentIndex(1)
            elif command == "right":
                self.inter.cobBoxTurnVeh.setCurrentIndex(2)

            stop_choice = settings["stop_choice"]
            if stop_choice == "normal":
                self.inter.cobBoxStopVeh.setCurrentIndex(0)
            elif stop_choice == "abrupt":
                self.inter.cobBoxStopVeh.setCurrentIndex(1)
            elif stop_choice == "penetrate":
                self.inter.cobBoxStopVeh.setCurrentIndex(2)
                self.pene.spinBoxDisDia.setValue(settings["penetrate_distance"])

            obey_traffic_lights = settings["obey_traffic_lights"]
            if obey_traffic_lights:
                self.inter.radButObeyVeh.setChecked(True)
            else:
                self.inter.radButObeyVeh.setChecked(False)

            safety_distance = settings["safety_distance"]
            self.inter.spinBoxSafeDisVeh.setValue(safety_distance)   

            vehicle_color = settings["vehicle_color"]
            RGB = vehicle_color.split(";")
            self.inter.lineEditRVeh.setText(RGB[0])
            self.inter.lineEditGVeh.setText(RGB[1])
            self.inter.lineEditBVeh.setText(RGB[2])

            if x == 0:
                lane_string = "subject"
            if x == 1:
                lane_string = "left"
            if x == 2:
                lane_string = "ahead"
            if x == 3:
                lane_string = "right"
            name = "car_inter" + str(self.cur_inter + 1) + "_" + lane_string + "_" + str(y + 1)

            self.inter.CarNameVeh.setText(name)
            tmpWidget = None
            for i in self.inter.widgets:
                if not i.isHidden():
                    tmpWidget = i
            self.inter.widgetVeh.show()
            if tmpWidget != None:
                tmpWidget.hide()
        return any_vehicle

    #vehicle page back to intersection page
    def vehicle_inter(self):
        self.inter.widgetVeh.hide()
        self.inter.widgetInt.show()

    #open traffic light dialogue
    def OpenTrafLit(self, num):
        #preset the boxes
        self.cur_light = num
        tmp = 0.00
        
        if self.light_list_all[self.cur_inter][self.cur_light][0] == tmp:
            self.TrafLit.cobBox1TLDia.setCurrentIndex(0)
            self.TrafLit.SpinBox1TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][1] - self.light_list_all[self.cur_inter][self.cur_light][0])
            tmp = self.light_list_all[self.cur_inter][self.cur_light][1]
        elif self.light_list_all[self.cur_inter][self.cur_light][2] == tmp:
            self.TrafLit.cobBox1TLDia.setCurrentIndex(1)
            self.TrafLit.SpinBox1TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][3] - self.light_list_all[self.cur_inter][self.cur_light][2])
            tmp = self.light_list_all[self.cur_inter][self.cur_light][3]
        elif self.light_list_all[self.cur_inter][self.cur_light][4] == tmp:
            self.TrafLit.cobBox1TLDia.setCurrentIndex(2)
            self.TrafLit.SpinBox1TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][5] - self.light_list_all[self.cur_inter][self.cur_light][4])
            tmp = self.light_list_all[self.cur_inter][self.cur_light][5]

        if self.light_list_all[self.cur_inter][self.cur_light][0] == tmp:
            self.TrafLit.cobBox2TLDia.setCurrentIndex(0)
            self.TrafLit.SpinBox2TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][1] - self.light_list_all[self.cur_inter][self.cur_light][0])
            tmp = self.light_list_all[self.cur_inter][self.cur_light][1]
        elif self.light_list_all[self.cur_inter][self.cur_light][2] == tmp:
            self.TrafLit.cobBox2TLDia.setCurrentIndex(1)
            self.TrafLit.SpinBox2TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][3] - self.light_list_all[self.cur_inter][self.cur_light][2])
            tmp = self.light_list_all[self.cur_inter][self.cur_light][3]
        elif self.light_list_all[self.cur_inter][self.cur_light][4] == tmp:
            self.TrafLit.cobBox2TLDia.setCurrentIndex(2)
            self.TrafLit.SpinBox2TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][5] - self.light_list_all[self.cur_inter][self.cur_light][4])
            tmp = self.light_list_all[self.cur_inter][self.cur_light][5]
        
        if self.light_list_all[self.cur_inter][self.cur_light][0] == tmp:
            self.TrafLit.cobBox3TLDia.setCurrentIndex(0)
            self.TrafLit.SpinBox3TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][1] - self.light_list_all[self.cur_inter][self.cur_light][0])
        elif self.light_list_all[self.cur_inter][self.cur_light][2] == tmp:
            self.TrafLit.cobBox3TLDia.setCurrentIndex(1)
            self.TrafLit.SpinBox3TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][3] - self.light_list_all[self.cur_inter][self.cur_light][2])
        elif self.light_list_all[self.cur_inter][self.cur_light][4] == tmp:
            self.TrafLit.cobBox3TLDia.setCurrentIndex(2)
            self.TrafLit.SpinBox3TLDia.setValue(self.light_list_all[self.cur_inter][self.cur_light][5] - self.light_list_all[self.cur_inter][self.cur_light][4])

        self.TrafLit.show()

    #open add vehicle dialogue
    def OpenAddVeh(self, num):
        self.cur_lane = num
        if self.cur_inter == 0 and self.cur_lane == 0 and not self.ego_spawned:
            self.addVeh.cobBoxTypeAdDia.setEnabled(True)
        else:
            self.addVeh.cobBoxTypeAdDia.setCurrentIndex(1)
            self.addVeh.cobBoxTypeAdDia.setEnabled(False)
        self.addVeh.show()

    #change front page collision
    def collision_change(self, state):
            self.collision = self.inter.checkBoxColFro.isChecked()

    #change front page max speed(navigation speed)
    def Max_speed_set(self):
        num = self.inter.spinBoxMaxVFro.value()
        num = (num * 1000) / 3600
        self.navigation_speed = num
        for i in self.intersection_list:
            i.navigation_speed = num

    #change front page safety distance
    def safety_distance_set(self):
        num = self.inter.spinBoxSafDisFro.value()
        self.gloSafetyDistance = num
        self.safety_distance = num

    #cancel the number of intersection input for error message dialogue
    def cancel_numInt(self):
        self.inter.spinBoxNumIntFro.setReadOnly(False)
        self.inter.spinBoxNumIntFro.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    
    #normal cancel for error message dialogue
    def usual_cancel(self):
        self.errMes.hide()

    #ok button on traffic light dialogue, set the backend traffic light
    def traffic_light_ok(self):
        red_start = self.light_list_all[self.cur_inter][self.cur_light][0]
        red_end = self.light_list_all[self.cur_inter][self.cur_light][1]
        yellow_start = self.light_list_all[self.cur_inter][self.cur_light][2]
        yellow_end = self.light_list_all[self.cur_inter][self.cur_light][3]
        green_start = self.light_list_all[self.cur_inter][self.cur_light][4]
        green_end = self.light_list_all[self.cur_inter][self.cur_light][5]
        tmp = 0.00

        #if user choose same light duration, show error message
        if self.TrafLit.cobBox1TLDia.currentIndex() == self.TrafLit.cobBox2TLDia.currentIndex() or \
        self.TrafLit.cobBox1TLDia.currentIndex() == self.TrafLit.cobBox3TLDia.currentIndex() or \
        self.TrafLit.cobBox2TLDia.currentIndex() == self.TrafLit.cobBox3TLDia.currentIndex():
            self.errMes.labelErr.setText("Three option of traffic light must be different")
            self.errMes.buttonBoxErr.accepted.connect(self.usual_cancel)
            self.errMes.buttonBoxErr.rejected.connect(self.usual_cancel)
            self.errMes.show()
            return
        
        if self.TrafLit.cobBox1TLDia.currentIndex() == 0:
            red_start = tmp
            red_end = red_start + self.TrafLit.SpinBox1TLDia.value()
            tmp = red_end
        elif self.TrafLit.cobBox1TLDia.currentIndex() == 1:
            yellow_start = tmp
            yellow_end = yellow_start + self.TrafLit.SpinBox1TLDia.value()
            tmp = yellow_end
        elif self.TrafLit.cobBox1TLDia.currentIndex() == 2:
            green_start = tmp
            green_end = green_start + self.TrafLit.SpinBox1TLDia.value()
            tmp = green_end

        if self.TrafLit.cobBox2TLDia.currentIndex() == 0:
            red_start = tmp
            red_end = red_start + self.TrafLit.SpinBox2TLDia.value()
            tmp = red_end
        elif self.TrafLit.cobBox2TLDia.currentIndex() == 1:
            yellow_start = tmp
            yellow_end = yellow_start + self.TrafLit.SpinBox2TLDia.value()
            tmp = yellow_end
        elif self.TrafLit.cobBox2TLDia.currentIndex() == 2:
            green_start = tmp
            green_end = green_start + self.TrafLit.SpinBox2TLDia.value()
            tmp = green_end
        
        if self.TrafLit.cobBox3TLDia.currentIndex() == 0:
            red_start = tmp
            red_end = red_start + self.TrafLit.SpinBox3TLDia.value()
        elif self.TrafLit.cobBox3TLDia.currentIndex() == 1:
            yellow_start = tmp
            yellow_end = yellow_start + self.TrafLit.SpinBox3TLDia.value()
        elif self.TrafLit.cobBox3TLDia.currentIndex() == 2:
            green_start = tmp
            green_end = green_start + self.TrafLit.SpinBox3TLDia.value()

        self.light_list_all[self.cur_inter][self.cur_light][0] = red_start
        self.light_list_all[self.cur_inter][self.cur_light][1] = red_end
        self.light_list_all[self.cur_inter][self.cur_light][2] = yellow_start
        self.light_list_all[self.cur_inter][self.cur_light][3] = yellow_end
        self.light_list_all[self.cur_inter][self.cur_light][4] = green_start
        self.light_list_all[self.cur_inter][self.cur_light][5] = green_end

        light_string = ""
        if self.cur_light == 0:
            light_string = "subject"
        if self.cur_light == 1:
            light_string = "left"
        if self.cur_light == 2:
            light_string = "ahead"
        if self.cur_light == 3:
            light_string = "right"

        self.intersection_list[self.cur_inter].edit_traffic_light(light_string, red_start, red_end, yellow_start, yellow_end, green_start, green_end)
        self.TrafLit.close()

    #ok button on add vehicle dialogue
    def add_vehicle_ok(self):
       
        index = self.addVeh.cobBoxModAdDia.currentIndex()
        gapNum = self.addVeh.spinBoxGapAdDia.value()
        model_combine = self.addVeh.model_list[index].split()
        R = self.addVeh.lineEditRDia.text()
        G = self.addVeh.lineEditGDia.text()
        B = self.addVeh.lineEditBDia.text()
        if R == "":
            R = "255"
        if G == "":
            G = "255"
        if B == "":
            B = "255"

        #check if user input a number between 0-255, if not, show error message 
        try:
            numR = int(R)
            numG = int(G)
            numB = int(B)
            if numR > 255 or numG > 255 or numB > 255:
                raise ValueError
        except ValueError:
            self.errMes.labelErr.setText("Please input a number between 0 and 255")
            self.errMes.show()
            self.errMes.buttonBoxErr.accepted.connect(self.usual_cancel)
            self.errMes.buttonBoxErr.rejected.connect(self.usual_cancel)
            return

        color = R + "," + G + "," + B
        model1 = model_combine[0]
        model2 = model_combine[1]
        Mname = "vehicle." + model1 + "." + model2
        choice_string = ""
        if self.cur_lane == 0:
            choice_string = "subject"
        elif self.cur_lane == 1:
            choice_string = "left"
        elif self.cur_lane == 2:
            choice_string = "ahead"
        elif self.cur_lane == 3:
            choice_string = "right"
        
        if self.cur_lane == 0 and self.cur_inter == 0:
            #special spawn process for init intersection 
            if self.addVeh.cobBoxTypeAdDia.currentIndex() == 0:
                car2 = self.intersection_list[self.cur_inter].add_ego_vehicle(gap=gapNum, model_name=Mname, safety_distance=self.gloSafetyDistance, vehicle_color=color)                
                car1 = self.intersection_list[self.cur_inter].add_lead_vehicle(lead_distance= 10, vehicle_color="255,255,255", safety_distance=self.gloSafetyDistance)
                car3 = self.intersection_list[self.cur_inter].add_follow_vehicle(follow_distance= 10, vehicle_color="255,255,255", safety_distance=self.gloSafetyDistance)
                 
                #put into car list for further use
                self.car_list[self.cur_inter][self.cur_lane].append(car1)
                self.car_list[self.cur_inter][self.cur_lane].append(car2)
                self.car_list[self.cur_inter][self.cur_lane].append(car3)

                self.ego_spawned = True
            else:
                if len(self.car_list[self.cur_inter][self.cur_lane]) == 0:
                    self.normal_num = 0
                else:
                    self.normal_num = 3
                car1 = self.intersection_list[self.cur_inter].add_vehicle(gap=gapNum, model_name=Mname, safety_distance=self.gloSafetyDistance, choice= choice_string, vehicle_color=color)
                self.car_list[self.cur_inter][self.cur_lane].append(car1)
        else:
            car1 = self.intersection_list[self.cur_inter].add_vehicle(gap=gapNum, model_name=Mname, safety_distance=self.gloSafetyDistance, choice= choice_string, vehicle_color=color)
            self.car_list[self.cur_inter][self.cur_lane].append(car1)
        self.show_car()

    #show car map
    def show_car(self):
        count = 0
        normal_count = 1
        RGB = None

        #show cars in subject lane
        for i in range(len(self.car_list[self.cur_inter][0])):
            name = "CarSub" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            if self.delete_car[self.cur_inter][0][i]:
                tmp.hide()
            else:
                uniqueName = self.car_list[self.cur_inter][0][i]
                settings = self.intersection_list[self.cur_inter].get_vehicle_settings(uniqueName)
                color = settings["vehicle_color"]
                if color != ";;" and color != None:
                    RGB = color.split(";")
                    tmp.setStyleSheet("background:rgb({},{},{}); color:{};".format(int(RGB[0]),int(RGB[1]),int(RGB[2]),(0,0,0)))
                tmp.show()
                if self.cur_inter == 0:
                    if i != self.normal_num:
                        if count == 0:
                            tmp.setText("Lead")
                        elif count == 1:
                            tmp.setText("Ego")
                        elif count == 2:
                            tmp.setText("Follow")
                        count += 1
                else:
                    tmp.setText(str(normal_count))
                    normal_count += 1

        #show cars in left lane
        for i in range(len(self.car_list[self.cur_inter][1])):
            name = "CarLeft" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            if self.delete_car[self.cur_inter][1][i]:
                tmp.hide()   
            else:
                uniqueName = self.car_list[self.cur_inter][1][i]
                settings = self.intersection_list[self.cur_inter].get_vehicle_settings(uniqueName)
                color = settings["vehicle_color"]
                RGB = color.split(";")           
                tmp.setStyleSheet("background:rgb({},{},{}); color:{};".format(int(RGB[0]),int(RGB[1]),int(RGB[2]),(0,0,0)))
                tmp.show()
        
        #show cars in ahead lane
        for i in range(len(self.car_list[self.cur_inter][2])):
            name = "CarAhead" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            if self.delete_car[self.cur_inter][2][i]:
                tmp.hide()
            else:
                uniqueName = self.car_list[self.cur_inter][2][i]
                settings = self.intersection_list[self.cur_inter].get_vehicle_settings(uniqueName)
                color = settings["vehicle_color"]
                RGB = color.split(";")
                tmp.setStyleSheet("background:rgb({},{},{}); color:{};".format(int(RGB[0]),int(RGB[1]),int(RGB[2]),(0,0,0)))
                tmp.show()

        #show cars in right lane
        for i in range(len(self.car_list[self.cur_inter][3])):       
            name = "CarRight" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            if self.delete_car[self.cur_inter][3][i]:
                tmp.hide()
            else:
                uniqueName = self.car_list[self.cur_inter][3][i]
                settings = self.intersection_list[self.cur_inter].get_vehicle_settings(uniqueName)
                color = settings["vehicle_color"]
                RGB = color.split(";")
                tmp.setStyleSheet("background:rgb({},{},{}); color:{};".format(int(RGB[0]),int(RGB[1]),int(RGB[2]),(0,0,0)))
                tmp.show()

    #delete car
    def deleteCar(self):
        self.intersection_list[self.cur_inter].remove_vehicle(self.cur_ID[0])       
        if self.cur_ID[1] == 0:
            car_string = "CarSub"
        elif self.cur_ID[1] == 1:
            car_string = "CarLeft"
        elif self.cur_ID[1] == 2:
            car_string = "CarAhead"
        elif self.cur_ID[1] == 3:
            car_string = "CarRight"
        
        name = car_string + str(self.cur_ID[2] + 1)
        tmp = self.inter.findChild(QLabel, name)
        middle = False

        #check if any more cars behind this one
        for i in range(self.cur_ID[2] + 1, 4):
            name = car_string + str(i + 1)
            tmp2 = self.inter.findChild(QLabel, name)
            if tmp2.isVisible():
                middle = True
        
        ###this part is to be coordinate with backend###
        #if there are, do not pop them yet
        if middle:
            tmp.hide()
            self.delete_car[self.cur_inter][self.cur_ID[1]][self.cur_ID[2]] = True
        else:
            #if not, pop from car list
            tmp.hide()
            self.car_list[self.cur_inter][self.cur_ID[1]].pop(self.cur_ID[2])

            #check if there are unpoped cars and pop them(due to middle car issue)
            for i in range(self.cur_ID[2] - 1, -1, -1):
                if self.delete_car[self.cur_inter][self.cur_ID[1]][i]:
                    self.car_list[self.cur_inter][self.cur_ID[1]].pop(i)
                    self.delete_car[self.cur_inter][self.cur_ID[1]][i] = False
                else:
                    break
        self.vehicle_inter()
    
    #clean the cars on map(not in car list)
    def clean_car(self):
        for i in range(4):
            name = "CarSub" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.hide()
        for i in range(4):
            name = "CarLeft" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.hide()
        for i in range(4):
            name = "CarAhead" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.hide()
        for i in range(4):
            name = "CarRight" + str(i + 1)
            tmp = self.inter.findChild(QLabel, name)
            tmp.hide()

    #confirm button on vehicle setting page 
    def confirm(self):
        turn = None
        choice_string = None
        stop = None
        car_string = None
        index = self.inter.cobBoxModVeh.currentIndex()
        model_combine = self.addVeh.model_list[index].split()
        model1 = model_combine[0]
        model2 = model_combine[1]
        Mname = "vehicle." + model1 + "." + model2

        if self.cur_lane == 0:
            choice_string = "subject"
        elif self.cur_lane == 1:
            choice_string = "left"
        elif self.cur_lane == 2:
            choice_string = "ahead"
        elif self.cur_lane == 3:
            choice_string = "right"

        if self.inter.cobBoxTurnVeh.currentIndex() == 0:
            turn = "straight"
        elif self.inter.cobBoxTurnVeh.currentIndex() == 1:
            turn = "left"
        elif self.inter.cobBoxTurnVeh.currentIndex() == 2:
            turn = "right"

        if self.inter.cobBoxStopVeh.currentIndex() == 0:
            stop = "normal"
        elif self.inter.cobBoxStopVeh.currentIndex() == 1:
            stop = "abrupt"
        elif self.inter.cobBoxStopVeh.currentIndex() == 2:
            stop = "penetrate" 
        
        R = self.inter.lineEditRVeh.text()
        G = self.inter.lineEditGVeh.text()
        B = self.inter.lineEditBVeh.text()

        #check if user input a number between 0-255, if not, show error message 
        try:
            numR = int(R)
            numG = int(G)
            numB = int(B)
            if numR > 255 or numG > 255 or numB > 255:
                raise ValueError
        except ValueError:
            self.errMes.labelErr.setText("Please input a number between 0 and 255")
            self.errMes.show()
            self.errMes.buttonBoxErr.accepted.connect(self.usual_cancel)
            self.errMes.buttonBoxErr.rejected.connect(self.usual_cancel)
            return

        if R == None:
            R = "0"
        if G == None:
            G = "0"
        if B == None:
            B = "0"
        color = R + "," + G + "," + B
        gap = self.inter.spinBoxGapVeh.value()
        safeDis = self.inter.spinBoxSafeDisVeh.value()
        state = self.inter.radButObeyVeh.isChecked()

        if self.cur_ID[1] == 0:
            car_string = "CarSub"
        elif self.cur_ID[1] == 1:
            car_string = "CarLeft"
        elif self.cur_ID[1] == 2:
            car_string = "CarAhead"
        elif self.cur_ID[1] == 3:
            car_string = "CarRight"

        name = car_string + str(self.cur_ID[2] + 1)
        tmp = self.inter.findChild(QLabel, name)
        tmp.setStyleSheet("background:rgb({},{},{}); color:{};".format(int(R),int(G),int(B),(0,0,0)))

        new_uniquename = self.intersection_list[self.cur_inter].edit_vehicle_settings(self.cur_ID[0], command=turn, stop_choice=stop, vehicle_color=color, gap=gap, safety_distance=safeDis, obey_traffic_lights=state, choice=choice_string, penetrate_distance=self.penetrate_dis, model_name=Mname)
        self.car_list[self.cur_inter][self.cur_ID[1]][self.cur_ID[2]] = new_uniquename
        self.vehicle_inter()

    #change between intersections
    def change_inter(self):
        self.clean_car()
        saved_file = self.intersection_list[self.cur_inter].export_settings()
        self.saved_intersections[self.cur_inter] = saved_file
        index = self.inter.cobBoxImportInt.findText("intersection " + str(self.cur_inter + 1))
        if index == -1:
            self.inter.cobBoxImportInt.addItem("intersection " + str(self.cur_inter + 1))
        self.cur_inter = self.inter.cobBoxIDInt.currentIndex() 
        self.show_car()
        self.inter.cobBoxImportInt.setCurrentIndex(0)

    #import intersection
    def import_inter(self):
        if self.inter.cobBoxImportInt.currentIndex() == 0:
            return
        self.clean_car()        
        import_string = self.inter.cobBoxImportInt.currentText()
        import_num = int(import_string.split()[1]) - 1
        new_intersection = self.intersection_list[self.cur_inter].import_settings(self.saved_intersections[import_num])

        for i in range(len(self.car_list[self.cur_inter])):
            for j in range(len(self.car_list[self.cur_inter][i])):
                self.car_list[self.cur_inter][i].pop()

        i = 0
        for vehicle_config in new_intersection["subject_vehicle"]:
            self.car_list[self.cur_inter][0].append(vehicle_config["uniquename"])
        for vehicle_config in new_intersection["left_vehicle"]:
            self.car_list[self.cur_inter][1].append(vehicle_config["uniquename"])
        for vehicle_config in new_intersection["ahead_vehicle"]:
            self.car_list[self.cur_inter][2].append(vehicle_config["uniquename"])
        for vehicle_config in new_intersection["right_vehicle"]:
            self.car_list[self.cur_inter][3].append(vehicle_config["uniquename"])
        
        self.show_car()
        tmp = self.light_list_all[import_num]
        self.light_list_all[self.cur_inter] = tmp

    #open simulation dialogue in front page
    def Front_simulation(self):
        self.simulation.show()

    #start simulation in front page
    def start_simulation(self):
        view_string = None
        self.setup_intersection_list()
        human = True
        if self.simulation.cobBoxViewSimDia.currentIndex() == 0:
            view_string = "first_person"
        elif self.simulation.cobBoxViewSimDia.currentIndex() == 1:
            view_string = "left"
        elif self.simulation.cobBoxViewSimDia.currentIndex() == 2:
            view_string = "human_driving"
        if self.simulation.cobBoxConSimDia.currentIndex() == 0:
            human = False
        IntersectionBackend(self.env, self.intersection_list, allow_collision = self.collision, spectator_mode = view_string, enable_human_control = human)

    #start penetration dialogue in vehicle setting page
    def Veh_penetrate(self):
        if self.inter.cobBoxStopVeh.currentIndex() == 2:
            self.pene.show()

    #ok on penetration dialogue
    def Veh_penetrate_ok(self):
        self.penetrate_dis = self.pene.spinBoxDisDia.value()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
