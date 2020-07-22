#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:24:10 2020

@author: shijiliu
"""


import sys
sys.path.append("..")

import carla
from backend.carla_env import CARLA_ENV 
import math
import time
import numpy as np
from configobj import ConfigObj
from backend.generate_path_omit_regulation import generate_path
from backend.intersection_definition import smooth_trajectory, get_trajectory
from scipy.interpolate import UnivariateSpline
import copy

from backend.section_definition import Section


# define a class for defining the initial section
# add vehicles is allowed in this section
class InitSection(Section):
    def __init__(self, env, world_waypoint):
        super().__init__(env, world_waypoint)
        
    def get_full_path_trajectory(self, subject_trajectory, subject_ref_speed, left_trajectory, left_ref_speed):
        '''
        

        Parameters
        ----------
        subject_trajectory : list, [(float, float), ... ]
            the subject trajectory.
        subject_ref_speed : list 
            reference speed for subject trajectory  
        left_trajectory : list, [(float, float), ... ]
            the left trajectory.
        left_ref_speed : list 
            reference speed for left trajectory

        Returns
        -------
        None.

        '''
        self.subject_trajectory = subject_trajectory
        self.subject_ref_speed = subject_ref_speed
        self.left_trajectory = left_trajectory
        self.left_ref_speed = left_ref_speed
    
    def add_ego_vehicle(self, model_name = "vehicle.tesla.model3", safety_distance = 15.0, vehicle_color = None):
        '''
        add ego vehicle to the initial intersection
        according to the user case, the ego vehicle will follow the 
        subject lane all the way with constant speed
        
        Parameters
        ----------
        model_name : string, optional
            vehicle type. The default is "vehicle.tesla.model3".
        safety_distance : float, optional
            smallest distance between this vehicle and vehicle ahead
        vehicle_color : string
            the RGB representation of the vehicle color. e.g. '255,255,255'

        Returns
        -------
        uniquename : string
            the name of the vehicle

        '''
        vehicle = ConfigObj()
        vehicle["model"] = model_name
        vehicle["safety_distance"] = safety_distance
        
        new_ref_waypoint = self.subject_waypoint
        spawn_transform = new_ref_waypoint.transform
        spawn_location = spawn_transform.location
        spawn_rotation = spawn_transform.rotation
        
        spawn_location = carla.Location(x = spawn_location.x, y = spawn_location.y, z = spawn_location.z + 0.1)
        
        uniquename = self.env.spawn_vehicle(model_name = model_name,spawn_point = carla.Transform(spawn_location,spawn_rotation), color = vehicle_color)
        vehicle["uniquename"] = uniquename
        vehicle["ref_waypoint"] = new_ref_waypoint
        vehicle["location"] = spawn_transform.location
        vehicle["rotation"] = spawn_transform.rotation
        
        if vehicle_color == None:
            vehicle["vehicle_color"] = vehicle_color
        else:
            vehicle["vehicle_color"] = vehicle_color.replace(',',';') # replace , by ; to avoid error when importing from file
        
        vehicle["trajectory"] = self.subject_trajectory
        vehicle["ref_speed_list"] = self.subject_ref_speed
        
        new_bb = self.env.get_vehicle_bounding_box(uniquename)
        vehicle["bounding_box"] = new_bb
        vehicle["vehicle_type"] = "ego"
        
        # additional settings that's necessary for using the VehicleControl class
        vehicle["stop_choice"] = None
        vehicle["penetrate_distance"] = None
        vehicle["stop_ref_point"] = None
        
        vehicle["gap"] = None
        vehicle["command"] = None
        vehicle["obey_traffic_lights"] = False
        vehicle["traffic_light"] = False
        vehicle["run"] = True
        vehicle["choice"] = None
        
        self.ego_vehicle = vehicle
        return uniquename
    
    def add_full_path_vehicle(self):
        pass