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
        self.left_ref_waypoint = self._get_left_waypoint(self.subject_waypoint)
        
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
        self.subject_max_speed_list = subject_ref_speed / 0.75
        self.subject_min_speed_list = subject_ref_speed / 0.75 * 0.5
        self.left_trajectory = left_trajectory
        self.left_ref_speed = left_ref_speed
        self.left_max_speed_list = left_ref_speed / 0.75
        self.left_min_speed_list = left_ref_speed / 0.75 * 0.5
    
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
    
    
    
    
    
    def edit_ego_vehicle(self, model_name = "vehicle.tesla.model3", safety_distance = 15.0, vehicle_color = None):
        '''
        edit the ego vheicle setting by delete the original ego vehicle and add a new one
        
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
        # get the original uniquename
        original_uniquename = self.ego_vehicle["uniquename"]
        
        # remove the ego vehicle
        self.env.destroy_vehicle(original_uniquename)
        self.ego_vehicle = None
        
        # add the new ego vehicle
        uniquename = self.add_ego_vehicle(model_name = model_name, safety_distance = safety_distance, vehicle_color = vehicle_color)
        return uniquename
    
    def remove_full_path_vehicle(self, uniquename):
        '''
        remove a full path vehicle based on its uniquename

        Parameters
        ----------
        uniquename : string
            name of the vehicle.

        Returns
        -------
        Bool : whether the given vehicle is found and removed
        
        vehicle_type : string
            the vehicle type, valid values are "lead", "follow"
        
        choice : string
            the lane choice, valid values are "subject", "left" 
            
        index : int
            the index of the vehicle in a specific lane

        '''
        vehicle_set = self.subject_lead_vehicle
        for jj in range(len(vehicle_set) - 1,-1,-1):
            vehicle = vehicle_set[jj]
            if vehicle["uniquename"] == uniquename:
                self.env.destroy_vehicle(uniquename)
                vehicle_set.pop(jj)
                return True, "lead", "subject", jj
        
        vehicle_set = self.subject_follow_vehicle
        for jj in range(len(vehicle_set) - 1,-1,-1):
            vehicle = vehicle_set[jj]
            if vehicle["uniquename"] == uniquename:
                self.env.destroy_vehicle(uniquename)
                vehicle_set.pop(jj)
                return True, "follow", "subject", jj
        
        vehicle_set = self.left_lead_vehicle
        for jj in range(len(vehicle_set) - 1,-1,-1):
            vehicle = vehicle_set[jj]
            if vehicle["uniquename"] == uniquename:
                self.env.destroy_vehicle(uniquename)
                vehicle_set.pop(jj)
                return True, "lead", "left", jj
        
        vehicle_set = self.left_follow_vehicle
        for jj in range(len(vehicle_set) - 1,-1,-1):
            vehicle = vehicle_set[jj]
            if vehicle["uniquename"] == uniquename:
                self.env.destroy_vehicle(uniquename)
                vehicle_set.pop(jj)
                return True, "follow", "left", jj
            
        return False, None, None, None
    
    
    def add_full_path_vehicle(self, model_name = "vehicle.tesla.model3", vehicle_type ="lead", choice = "subject", command = "speed", command_start_time = 0.0, gap = 10.0, safety_distance = 15.0, lead_follow_distance = 20.0, vehicle_color = None):
        '''
        add full path vehicle

        Parameters
        ----------
        model_name : string, optional
            vehicle type. The default is "vehicle.tesla.model3".
        vehicle_type : string, optional
            the vehicle type, valid values : "lead", "follow". The default is "lead".
        choice : string, optional
            the lane choice, valid values are "subject", "left". The default is "subject".
        command : string, optional
            the command the vehicle is going to execute in this section. Valid values: "speed", "lane", "distance". The default is "speed".
        command_start_time : string, optional
            the time at which the command should be executed. The default is 0.0.
        gap : float, optional
            the gap between the vehicle and the one in the front of it when adding. The default is 10.0, unit: meter
        safety_distance : float, optional
            smallest distance between 2 vehicles when simulation is going. The default is 15.0, unit: meter
        vehicle_color : string
            the RGB representation of the vehicle color. e.g. '255,255,255'

        Returns
        -------
        uniquename : string
            the name of the vehicle


        '''
        # create configuration file for vehicle
        vehicle = ConfigObj()
        vehicle["model"] = model_name
        vehicle["safety_distance"] = safety_distance
        vehicle["gap"] = gap
        vehicle["command"] = command
        vehicle["command_start_time"] = command_start_time
        vehicle["run"] = True
        vehicle["choice"] = choice
        vehicle["current_lane"] = choice # which lane the vehicle is currently in
        vehicle["vehicle_type"] = vehicle_type 
        vehicle["lead_follow_distance"] = lead_follow_distance
        
        vehicle["stop_choice"] = None
        vehicle["penetrate_distance"] = None
        vehicle["stop_ref_point"] = None
        vehicle["obey_traffic_lights"] = False
        vehicle["traffic_light"] = False
        
        vehicle_set = None
        ref_waypoint = None
        vehicle["trajectory"] = None
        vehicle["ref_speed_list"] = None
        
        # get the vehicle set by input parameters, so as to create add the vehicle
        if vehicle_type == "lead" and choice == "subject":
            vehicle_set = self.subject_lead_vehicle
            ref_waypoint = self.subject_waypoint
            lane_direction = 1 # positive direction for lead
            vehicle["trajectory"] = self.subject_trajectory
            vehicle["ref_speed_list"] = self.subject_ref_speed
            
        elif vehicle_type == "lead" and choice == "left":
            vehicle_set = self.left_lead_vehicle
            ref_waypoint = self.left_ref_waypoint
            lane_direction = 1 # positive direction for lead
            vehicle["trajectory"] = self.left_trajectory
            vehicle["ref_speed_list"] = self.left_ref_speed
            
        elif vehicle_type == "follow" and choice == "subject":
            vehicle_set = self.subject_follow_vehicle
            ref_waypoint = self.subject_waypoint
            lane_direction = -1 # negative direction for follow
            vehicle["trajectory"] = self.subject_trajectory
            vehicle["ref_speed_list"] = self.subject_ref_speed
            
        elif vehicle_type == "follow" and choice == "left":
            vehicle_set = self.left_follow_vehicle
            ref_waypoint = self.left_ref_waypoint
            lane_direction = -1 # negative direction for follow
            vehicle["trajectory"] = self.left_trajectory
            vehicle["ref_speed_list"] = self.left_ref_speed
        
        
        
        
        # get the spawn location
        if len(vehicle_set) != 0:
            ref_waypoint = vehicle_set[-1]["ref_waypoint"]
            bb = vehicle_set[-1]["bounding_box"]
            gap += bb.x
        else:
            if gap < 10.0:
                gap = 10.0
        
        forward_vector = ref_waypoint.transform.get_forward_vector()

        location = ref_waypoint.transform.location
        raw_spawn_point = carla.Location(x = location.x + lane_direction * gap * forward_vector.x  , y = location.y + lane_direction *  gap * forward_vector.y , z = location.z + 0.1)
        
        new_ref_waypoint = self.carla_map.get_waypoint(raw_spawn_point)
        
        spawn_transform = new_ref_waypoint.transform
        spawn_location = spawn_transform.location
        spawn_rotation = spawn_transform.rotation
        
        spawn_location = carla.Location(x = spawn_location.x, y = spawn_location.y, z = spawn_location.z + 0.1)
        
        uniquename = self.env.spawn_vehicle(model_name = model_name,spawn_point = carla.Transform(spawn_location,spawn_rotation) , color = vehicle_color)
        
        vehicle["uniquename"] = uniquename
        vehicle["ref_waypoint"] = new_ref_waypoint
        vehicle["location"] = new_ref_waypoint.transform.location
        vehicle["rotation"] = new_ref_waypoint.transform.rotation
        
        if vehicle_color == None:
            vehicle["vehicle_color"] = vehicle_color
        else:
            vehicle["vehicle_color"] = vehicle_color.replace(',',';') # replace , by ; to avoid error when importing from file
        
        vehicle["subject_trajectory"] = self.subject_trajectory
        vehicle["subject_ref_speed_list"] = self.subject_ref_speed
        vehicle["subject_max_speed_list"] = self.subject_max_speed_list
        vehicle["subject_min_speed_list"] = self.subject_min_speed_list
        vehicle["left_trajectory"] = self.left_trajectory
        vehicle["left_ref_speed_list"] = self.left_ref_speed
        vehicle["left_max_speed_list"] = self.left_max_speed_list
        vehicle["left_min_speed_list"] = self.left_min_speed_list
        
        new_bb = self.env.get_vehicle_bounding_box(uniquename)
        vehicle["bounding_box"] = new_bb
        
        vehicle_set.append(vehicle)
        
        return uniquename
    
    def edit_full_path_vehicle(self, uniquename, vehicle_type, choice, model_name = "vehicle.tesla.model3",   command = "speed", command_start_time = 0.0, gap = 10.0, safety_distance = 25.0, lead_follow_distance = 30.0, vehicle_color = None):
        '''
        edit full path vehicle settings by deleting the original vehicle and then add a new one

        Parameters
        ----------
        uniquename : string
            the name of the vehicle
        vehicle_type : string, 
            the vehicle type, valid values : "lead", "follow". 
        choice : string, optional
            the lane choice, valid values are "subject", "left". 
        model_name : string, optional
            vehicle type. The default is "vehicle.tesla.model3".
        command : string, optional
            the command the vehicle is going to execute in this section. Valid values: "speed", "lane", "distance". The default is "speed".
        command_start_time : string, optional
            the time at which the command should be executed. The default is 0.0.
        gap : float, optional
            the gap between the vehicle and the one in the front of it when adding. The default is 10.0, unit: meter
        safety_distance : float, optional
            smallest distance between 2 vehicles when simulation is going. The default is 15.0, unit: meter
        vehicle_color : string
            the RGB representation of the vehicle color. e.g. '255,255,255'

        Returns
        -------
        new_uniquename : string
            the new_name of the vehicle

        index: int
            the index of the vehicle to be changed

        '''
        if vehicle_type == "lead" and choice == "subject":
            vehicle_set = self.subject_lead_vehicle
            lane_direction = 1 # positive direction for lead

            
        elif vehicle_type == "lead" and choice == "left":
            vehicle_set = self.left_lead_vehicle
            lane_direction = 1 # positive direction for lead
            
        elif vehicle_type == "follow" and choice == "subject":
            vehicle_set = self.subject_follow_vehicle
            lane_direction = -1 # negative direction for follow
            
        elif vehicle_type == "follow" and choice == "left":
            vehicle_set = self.left_follow_vehicle
            lane_direction = -1 # negative direction for follow
            
        # get vehicle index in the given lane
        index = 0
        original_gap = None
        for vehicle in vehicle_set:
            if vehicle["uniquename"] == uniquename:
                original_gap = vehicle["gap"]
                break
            index += 1
            
        # shift the vehicle
        if original_gap != None:
            shift_distance = original_gap - gap
            self._shift_vehicles(shift_distance, vehicle_type = vehicle_type , choice = choice, index = index)
        else:
            print("return None in edit vehicle")
            return None
        
        # remove the current vehicle, 
        # note that after removing the vehicle, index is pointing at the vehicle after the current one
        removed, _, _, _ = self.remove_full_path_vehicle(uniquename)
        if not removed:
            print("vehicle not found")
            return None
        
        # split the vehicle set
        if vehicle_type == "lead" and choice == "subject":
            vehicles_after_current = self.subject_lead_vehicle[index:]
            self.subject_lead_vehicle = self.subject_lead_vehicle[:index]

            
        elif vehicle_type == "lead" and choice == "left":
            vehicles_after_current = self.left_lead_vehicle[index:]
            self.left_lead_vehicle = self.left_lead_vehicle[:index]

            
        elif vehicle_type == "follow" and choice == "subject":
            vehicles_after_current = self.subject_follow_vehicle[index:]
            self.subject_follow_vehicle = self.subject_follow_vehicle[:index]

            
        elif vehicle_type == "follow" and choice == "left":
            vehicles_after_current = self.left_follow_vehicle[index:]
            self.left_follow_vehicle = self.left_follow_vehicle[:index]

        
        # add the new vehicle
        new_uniquename = self.add_full_path_vehicle(model_name = model_name, 
                                                    vehicle_type = vehicle_type, 
                                                    choice = choice, 
                                                    command = command, 
                                                    command_start_time = command_start_time, 
                                                    gap = gap, safety_distance = safety_distance, 
                                                    lead_follow_distance = lead_follow_distance, 
                                                    vehicle_color = vehicle_color)
        
        # put back the vehicles after the current one
        if vehicle_type == "lead" and choice == "subject":
            self.subject_lead_vehicle += vehicles_after_current

            
        elif vehicle_type == "lead" and choice == "left":
            self.left_lead_vehicle += vehicles_after_current

            
        elif vehicle_type == "follow" and choice == "subject":
            self.subject_follow_vehicle += vehicles_after_current

            
        elif vehicle_type == "follow" and choice == "left":
            self.left_follow_vehicle += vehicles_after_current
            
        return new_uniquename, index
    
    
    def _shift_vehicles(self, length, vehicle_type, choice, index = 0):
        '''
        shift the vehicle starting at "index" in a specific lane specified by the
        vehicle_type and choice

        Parameters
        ----------
        length : float
            the length these vehicles will be moved. Positive value moves vehicles away from the ego
        vehicle_type : string, 
            the vehicle type, valid values : "lead", "follow". 
        choice : string, 
            the lane choice, valid values are "subject", "left". 
        index : int
            the index of the vehicle inside a specific lane.  default is 0

        Returns
        -------
        None.

        '''
        if vehicle_type == "lead" and choice == "subject":
            vehicle_set = self.subject_lead_vehicle
            lane_direction = 1 # positive direction for lead

            
        elif vehicle_type == "lead" and choice == "left":
            vehicle_set = self.left_lead_vehicle
            lane_direction = 1 # positive direction for lead
            
        elif vehicle_type == "follow" and choice == "subject":
            vehicle_set = self.subject_follow_vehicle
            lane_direction = -1 # negative direction for follow
            
        elif vehicle_type == "follow" and choice == "left":
            vehicle_set = self.left_follow_vehicle
            lane_direction = -1 # negative direction for follow
    
        for ii in range(len(vehicle_set) - 1,index - 1,-1):
            vehicle = vehicle_set[ii]
            new_ref_waypoint = self._get_next_waypoint(vehicle["ref_waypoint"],distance = length * lane_direction) # get the new
                                                                                                                   # reference point
            new_ref_location = new_ref_waypoint.transform.location          

            spawn_location = carla.Location(x = new_ref_location.x, y = new_ref_location.y, z = new_ref_location.z + 0.1)  
            spawn_rotation = new_ref_waypoint.transform.rotation
                                                                            
            self.env.move_vehicle_location(vehicle["uniquename"],carla.Transform(spawn_location,spawn_rotation))
            vehicle["ref_waypoint"] = new_ref_waypoint
            vehicle["location"] = spawn_location
            vehicle["rotation"] = spawn_rotation
            
        
    
    def _get_unit_left_vector(self,yaw):
        # get the right vector
        right_yaw = (yaw + 90) % 360
        rad_yaw = math.radians(right_yaw)
        right_vector = [math.cos(rad_yaw),math.sin(rad_yaw)]
        right_vector = right_vector / np.linalg.norm(right_vector)
        return right_vector
    
    
    def _get_left_waypoint(self, curr_waypoint):
        # get the point to the left of the current one
        left_shift = 3.0
        
        curr_location = curr_waypoint.transform.location
        ref_yaw = curr_waypoint.transform.rotation.yaw
        left_vector = self._get_unit_left_vector(ref_yaw)
    
        new_location = carla.Location(x = curr_location.x - left_shift * left_vector[0], y = curr_location.y - left_shift * left_vector[1], z = curr_location.z)
        
        left_waypoint = self.carla_map.get_waypoint(new_location)
        return left_waypoint
    
    def _get_next_waypoint(self,curr_waypoint,distance = 10):
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