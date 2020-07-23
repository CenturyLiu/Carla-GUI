#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 09:58:37 2020

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

# color for debug use
red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)

# the definition of the normal section
class Section(object):
    def __init__(self, env, world_waypoint):
        '''
        

        Parameters
        ----------
        env : CARLA_ENV
            the simulation environment
        world_waypoint : carla.Waypoint
            the subject point of the section.

        Returns
        -------
        None.

        '''
        # store the environment
        self.env = env
        
        
        # get the world map
        self.carla_map = self.env.world.get_map()
        
        # get the central point of the Section, which will be the reference for subject waypoint 
        self.subject_waypoint = world_waypoint
        
        self.section_location = self.subject_waypoint.transform.location
        
        # get the reference points of the Section, which will be used to form trajectory
        self._get_section_trajectory_points()
        
        # variable for storing the vehicles in subject lane and left lane
        self.subject_lead_vehicle = [] # for normal section, adding vehicle is currently not allowed
        self.subject_follow_vehicle = []
        self.left_lead_vehicle = []  # vehicles will be loaded in from init sections
        self.left_follow_vehicle = []
        self.ego_vehicle = None
            
        # variable for storing the trajectory for subject lane and left lane
        self.subject_trajectory = None # these two variables are currently not put into use
        self.left_trajectory = None # keep these variables in case adding section only vehicles is allowed in the future
    
    
        # variable to count the time elapsed after simulation starts in this section
        self.time_count = 0
    
    def _get_next_waypoint(self,curr_waypoint,distance = 4):
        '''
        

        Parameters
        ----------
        curr_waypoint : carla.Waypoint
            current waypoint.
        distance : float, optional
            "distance" between current waypoint and target waypoint . The default is 10.

        Returns
        -------
        next_waypoint : carla.Waypoint
            next waypoint, "distance" away from curr_waypoint, in the direction of the current way point
        '''
        forward_vector = curr_waypoint.transform.get_forward_vector()

        location = curr_waypoint.transform.location
        raw_spawn_point = carla.Location(x = location.x + distance * forward_vector.x  , y = location.y + distance * forward_vector.y , z = location.z + 0.1)
        
        next_waypoint = self.carla_map.get_waypoint(raw_spawn_point)
        return next_waypoint
    
    def _get_section_trajectory_points(self):
        '''
        get the reference points for trajectory

        Returns
        -------
        None.

        '''
        
        reference_way_points = []
        curr_waypoint = self.subject_waypoint
        
        # points after the subject, for adding follow vehicles
        for ii in range(8):
            distance = -4
            next_waypoint = self._get_next_waypoint(curr_waypoint, distance = distance)
            reference_way_points.append(next_waypoint)
            curr_waypoint = next_waypoint
            
        # points before the subject, for adding lead vehicles and navigation
        
        reference_way_points.reverse()
        reference_way_points.append(self.subject_waypoint)
        curr_waypoint = self.subject_waypoint
        
        for ii in range(90):
            distance = 4
            next_waypoint = self._get_next_waypoint(curr_waypoint, distance = distance)
            reference_way_points.append(next_waypoint)
            curr_waypoint = next_waypoint
            
        self.reference_way_points = reference_way_points
        
    def _add_full_path_vehicle_normal(self, uniquename, vehicle_type, choice, command = "speed", command_start_time = 0.0):
        '''
        Create a setting place holder of the vehicle that has been added to the initial section
        The command and command start time will be kept as default
        
        Front end user should not use this function

        Parameters
        ----------
        uniquename : string
            the name of the vehicle
        vehicle_type : string, 
            the vehicle type, valid values : "lead", "follow". 
        choice : string, 
            the lane choice, valid values are "subject", "left". 
        command : string, optional
            the command the vehicle is going to execute in this section. Valid values: "speed", "lane", "distance". The default is "speed".
        command_start_time : string, optional
            the time at which the command should be executed. The default is 0.0.

        Returns
        -------
        None.

        '''
        if vehicle_type == "lead" and choice == "subject":
            vehicle_set = self.subject_lead_vehicle
            
        elif vehicle_type == "lead" and choice == "left":
            vehicle_set = self.left_lead_vehicle
            
        elif vehicle_type == "follow" and choice == "subject":
            vehicle_set = self.subject_follow_vehicle
            
        elif vehicle_type == "follow" and choice == "left":
            vehicle_set = self.left_follow_vehicle
            
        vehicle_local_config = ConfigObj()
        vehicle_local_config["uniquename"] = uniquename
        vehicle_local_config["command"] = command
        vehicle_local_config["command_start_time"] = command_start_time
        
        vehicle_set.append(vehicle_local_config)
    
    def _update_vehicle_uniquename(self, vehicle_type, choice, index, uniquename):
        '''
        Private function for updating the uniquename of the vehicle in case uniquename is changed

        Parameters
        ----------
        vehicle_type : string, 
            the vehicle type, valid values : "lead", "follow". 
        choice : string, 
            the lane choice, valid values are "subject", "left". 
        index : int
            the index of the vehicle inside a specific lane. 
        uniquename : string
            the name of the vehicle

        Returns
        -------
        None.

        '''
        if vehicle_type == "lead" and choice == "subject":
            vehicle_set = self.subject_lead_vehicle
            
        elif vehicle_type == "lead" and choice == "left":
            vehicle_set = self.left_lead_vehicle
            
        elif vehicle_type == "follow" and choice == "subject":
            vehicle_set = self.subject_follow_vehicle
            
        elif vehicle_type == "follow" and choice == "left":
            vehicle_set = self.left_follow_vehicle
            
        if len(vehicle_set) <= index:
            print("Invalid index")
            return
        
        vehicle_local_config = vehicle_set[index]
        vehicle_local_config["uniquename"] = uniquename
    
    def edit_full_path_vehicle_local_setting(self, vehicle_type, choice, index , command = "speed", command_start_time = 0.0):
        '''
        API for the users to edit settings of a given vehicle 

        Parameters
        ----------
        vehicle_type : string, 
            the vehicle type, valid values : "lead", "follow". 
        choice : string, 
            the lane choice, valid values are "subject", "left". 
        index : int
            the index of the vehicle inside a specific lane. 
        command : string, optional
            the command the vehicle is going to execute in this section. Valid values: "speed", "lane", "distance". The default is "speed".
        command_start_time : string, optional
            the time at which the command should be executed. The default is 0.0.

        Returns
        -------
        None.

        '''
        if vehicle_type == "lead" and choice == "subject":
            vehicle_set = self.subject_lead_vehicle
            
        elif vehicle_type == "lead" and choice == "left":
            vehicle_set = self.left_lead_vehicle
            
        elif vehicle_type == "follow" and choice == "subject":
            vehicle_set = self.subject_follow_vehicle
            
        elif vehicle_type == "follow" and choice == "left":
            vehicle_set = self.left_follow_vehicle
        
        if len(vehicle_set) <= index:
            print("Invalid index")
            return
        
        vehicle_local_config = vehicle_set[index]
        vehicle_local_config["command"] = command
        vehicle_local_config["command_start_time"] = command_start_time
    
    def get_full_path_vehicle_local_setting(self, vehicle_type, choice, index):
        # get the settings of the vehicle based on lane and index
        # return the command and corresponding start time
        if vehicle_type == "lead" and choice == "subject":
            vehicle_set = self.subject_lead_vehicle
            
        elif vehicle_type == "lead" and choice == "left":
            vehicle_set = self.left_lead_vehicle
            
        elif vehicle_type == "follow" and choice == "subject":
            vehicle_set = self.subject_follow_vehicle
            
        elif vehicle_type == "follow" and choice == "left":
            vehicle_set = self.left_follow_vehicle
        
        if len(vehicle_set) <= index:
            print("Invalid index")
            return None, None
        
        vehicle_local_config = vehicle_set[index]
        command = vehicle_local_config["command"]
        command_start_time = vehicle_local_config["command_start_time"]
        return command, command_start_time
    
    def get_section_trajectory_points(self):
        # get the reference points of this section for use outside
        return self.reference_way_points
        
    def tick(self):
        # increment the time_count by one step
        # return the elapsed time in terms of seconds
        ret_val = self.time_count * self.env.delta_seconds
        self.time_count += 1
        return ret_val
    
    def section_start(self, ego_transform):
        '''
        function deciding whether this section should start

        Parameters
        ----------
        ego_transform : carla.Transform
            the transform of the ego vehicle.

        Returns
        -------
        None.

        '''
        ego_location = ego_transform.location
        
        # get the distance between the ego vehicle and center of section
        distance_2d = math.sqrt( (ego_location.x - self.section_location.x) ** 2 + (ego_location.y - self.section_location.y) ** 2)
    
        if distance_2d < 3.0: # the ego vehicle is close enough to the section reference point
            return True
        else:
            return False
    