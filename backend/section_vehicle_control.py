#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 10:15:47 2020

@author: shijiliu
"""

import sys
sys.path.append("..")

import carla
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time
import math

import control # the python-control package, install first

from backend.intersection_definition import Intersection, get_traffic_lights
from carla_env import CARLA_ENV # self-written class that provides help functions, should be in the same folder
from configobj import ConfigObj
from backend.multiple_vehicle_control import VehicleControl

import copy


# color for debug use
red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)

class FullPathVehicleControl(VehicleControl):
    def __init__(self, env, vehicle_config, delta_seconds):
        super().__init__(env,vehicle_config,delta_seconds)
        
        # store the subject trajectory and left trajectory
        self.subject_trajectory = copy.copy(self.vehicle_config["subject_trajectory"])
        self.subject_ref_speed = copy.copy(self.vehicle_config["subject_ref_speed_list"])
        self.subject_max_ref_speed = copy.copy(self.vehicle_config["subject_max_speed_list"])
        self.subject_min_ref_speed = copy.copy(self.vehicle_config["subject_min_speed_list"])
        
        self.left_trajectory = copy.copy(self.vehicle_config["left_trajectory"])
        self.left_ref_speed = copy.copy(self.vehicle_config["left_ref_speed_list"])
        self.left_max_ref_speed = copy.copy(self.vehicle_config["left_max_speed_list"])
        self.left_min_ref_speed = copy.copy(self.vehicle_config["left_min_speed_list"])
        
        # store the current lane of the vehicle
        self.current_lane = copy.copy(self.vehicle_config["current_lane"])
        
        # store the local time of the section the vehicle is in
        self.local_time = 0.0
        
        # store the time the vehicle is going to take command, (command should be "lane")
        self.command_start_time = self.vehicle_config["command_start_time"]
        
        # store time steps after executing the change lane command
        self.lane_change_step = 0
        
        # store variable for deciding whether the vehicle should change lane
        self.lane_change_available = False
        
    def _change_lane(self):
        '''
        order the vehicle to change its lane

        Returns
        -------
        None.

        '''
        # check whether the vehicle is safe to change lane
        if not self.lane_change_available:
            if self.current_lane == "subject":
                has_vehicle_in_left, distance = self.env.check_vehicle_in_left(self.model_uniquename, safety_distance = 6)
                
                #print("--------")
                #print("has_vehicle_in_left : ", has_vehicle_in_left)
                #print("distance: ", distance)
                if has_vehicle_in_left:
                    if distance < 0:
                        self.ref_speed_list = copy.copy(self.subject_max_ref_speed) # accelerate to max speed if the close vehicle is behind
                                                                                    # the current vehicle
                    else:
                        self.ref_speed_list = copy.copy(self.subject_min_ref_speed) # deccelerate to min speed if the close vehicle is in
                                                                                    # front of the current vehicle
                    return # only change speed, don't change lane
                else:
                    self.lane_change_available = True # no close vehicle in left lane, enable lane change
            else:
                # vehicle currently in right lane
                has_vehicle_in_right, distance = self.env.check_vehicle_in_right(self.model_uniquename, safety_distance = 6)
                
                #print("--------")
                #print("has_vehicle_in_right : ", has_vehicle_in_right)
                #print("distance: ", distance)
                
                if has_vehicle_in_right:
                    if distance < 0:
                        self.ref_speed_list = copy.copy(self.left_max_ref_speed) # accelerate to max speed if the close vehicle is behind
                                                                                    # the current vehicle
                    else:
                        self.ref_speed_list = copy.copy(self.left_min_ref_speed) # deccelerate to min speed if the close vehicle is in
                                                                                 # front of the current vehicle
                    return # only change speed, don't change lane                                                   
                else:
                    self.lane_change_available = True # no close vehicle in left lane, enable lane change
        
        
        
        if self.lane_change_step == 0:
            if self.current_lane == "subject":
                self.trajectory = copy.copy(self.left_trajectory)
                self.ref_speed_list = copy.copy(self.left_ref_speed)
                self.current_lane = "left"
            else:
                self.trajectory = copy.copy(self.subject_trajectory)
                self.ref_speed_list = copy.copy(self.subject_ref_speed)
                self.current_lane = "subject"
            self.lane_change_step += 1
            self.Lfc = 15.0 # set a large look ahead distance when changing the lane
        elif self.lane_change_step > 0 and self.lane_change_step < 15:
            self.lane_change_step += 1
        else:
            self.command = "speed" # have changed the lane, change the mode to speed
            self.lane_change_step = 0
            self.Lfc = 4.0 # change the look ahead distance back to its original value
            self.lane_change_available = False
        
    def update_local_time(self, local_time):
        # update the local time of the section the vehicle is in
        # the time is used to decide whether the vehicle is going to 
        # change direction
        self.local_time = local_time
        if self.command == "lane" and self.command_start_time <= self.local_time:
            self._change_lane()
    