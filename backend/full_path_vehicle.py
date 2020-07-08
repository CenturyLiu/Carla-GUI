#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 11:06:32 2020

@author: shijiliu
"""


import carla
import numpy as np
from collections import deque
import time
import math

import control # the python-control package, install first

from generate_path_omit_regulation import generate_path
from intersection_definition import Intersection, get_traffic_lights, get_trajectory, smooth_trajectory
from carla_env import CARLA_ENV # self-written class that provides help functions, should be in the same folder
from configobj import ConfigObj
from multiple_vehicle_control import VehicleControl

import copy

# color for debug use
red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)

class LeadVehicleControl(VehicleControl):
    # the LeadVehicleControl has two different modes:
    # normal full path mode: vehicle follows normal full path
    # pause mode: vehicle stop to the right of the lane,
    #             waiting for the ego vehicle to come
    
    def __init__(self,env,vehicle_config, delta_seconds):
        super().__init__(env, vehicle_config, delta_seconds)
        
        # copy the full path trajectory
        self.full_path_trajectory = copy.copy(self.trajectory)
        self.full_path_index = copy.copy(self.index)
        self.full_path_ref_speed_list = copy.copy(self.ref_speed_list )
        
        # generate waypoints for pausing the car
        self._get_pause_waypoints()
        self.mode = "normal"
        
    def _get_pause_waypoints(self):
        '''
        generate a list of waypoints for the pause path
        the waypoints are in vehicle right-hand coordinates, the heading 
        direction of the vehicle is x-axis

        Returns
        -------
        None.

        '''
        bb = self.vehicle_config["bounding_box"]
        self.pause_waypoint_list = [(0.0,0.0),(bb.x, -bb.y ),(bb.x * 2,-bb.y * 2),(bb.x * 3, -bb.y * 3),(bb.x * 4, -bb.y * 3.5),(bb.x * 5, -bb.y * 3.5),(bb.x * 6, -bb.y * 3.5),(bb.x * 7, -bb.y * 3.5)]
                                   #[(0.0,0.0),(2 * bb.x, 0.0),(bb.x * 3,bb.y / 2),(bb.x * 4, bb.y),(bb.x * 5, bb.y * 2),(bb.x * 6, bb.y * 2),(bb.x * 8, bb.y * 2)]
                                   #[(0.0,0.0),(bb.x, 0.0),(bb.x * 2,-bb.y / 2),(bb.x * 3, -bb.y),(bb.x * 4, -bb.y)]
        
    def _get_unit_left_vector(self,yaw):
        # get the left vector (y axis)
        right_yaw = (yaw + 90) % 360
        rad_yaw = math.radians(right_yaw)
        left_vector = np.array([math.cos(rad_yaw),math.sin(rad_yaw)])
        left_vector = left_vector / np.linalg.norm(left_vector)
        return left_vector
        
    def _generate_pause_path(self):
        '''
        generate a path for the vehicle to right shift a certain value and then stop.
        assume the lead vehicle is always heading in the straight direction

        Returns
        --
        None
        '''
        # get world transform of the lead vehicle
        world_transform = self.env.get_transform_3d(self.model_uniquename)
        location = world_transform.location
        location_2d = np.array([location.x,location.y])
        forward_vector = world_transform.get_forward_vector()
        forward_vector_2d = np.array([forward_vector.x,forward_vector.y])
        left_vector_2d =  self._get_unit_left_vector(world_transform.rotation.yaw)
        
        # transform local waypoints into global coordinates
        world_waypoints = []
        for pt in self.pause_waypoint_list:
            world_pt = location_2d + pt[0] * forward_vector_2d + pt[1] * left_vector_2d
            world_waypoints.append( ((world_pt[0],world_pt[1]),5.0) ) # vehicle will stop at 5 m/s
            if self.debug_vehicle:
                loc = carla.Location(x = world_pt[0],y = world_pt[1], z = 0.0)
                self.env.world.debug.draw_point(loc, size = 0.2, color = white, life_time=0.0, persistent_lines=True)
        
        # form trajectory
        smoothed_full_trajectory, ref_speed_list = get_trajectory(world_waypoints)
        
        self.pause_path_trajectory = smoothed_full_trajectory
        self.pause_path_ref_speed = ref_speed_list
        
        self.pause_path_index = 0
        
        if self.debug_vehicle:
            
            for ii in range(1,len(smoothed_full_trajectory)):
                loc1 = carla.Location(x = smoothed_full_trajectory[ii - 1][0], y = smoothed_full_trajectory[ii - 1][1], z = 0.0)
                loc2 = carla.Location(x = smoothed_full_trajectory[ii][0], y = smoothed_full_trajectory[ii][1], z = 0.0)
                self.env.world.debug.draw_arrow(loc1, loc2, thickness = 0.05, arrow_size = 0.1, color = red, life_time=0.0, persistent_lines=True)
        
    def change_mode(self, mode):
        '''
        change vehicle mode
        
        the LeadVehicleControl has two different modes:
        normal full path mode: vehicle follows normal full path
        pause mode: vehicle stop to the right of the lane,
                    waiting for the ego vehicle to come

        Parameters
        ----------
        mode : string
            the mode. valid valuse are "normal","pause"

        Returns
        -------
        None.

        '''
        if mode == "normal":
            self.index = copy.copy(self.full_path_index)
            self.ref_speed_list = copy.copy(self.full_path_ref_speed_list)
            self.trajectory = copy.copy(self.full_path_trajectory)
            self.mode = mode
        elif mode == "pause":
            self._generate_pause_path() # generate path when switching mode
            self.index = copy.copy(self.pause_path_index)
            self.ref_speed_list = copy.copy(self.pause_path_ref_speed)
            self.trajectory = copy.copy(self.pause_path_trajectory)
            self.mode = mode


    def pure_pursuit_control_wrapper(self):
        '''
        Apply one step control to the vehicle, store essential information for further use
        
        Note: this is an overriden version of pure_pursuit_control_wrapper
              to avoid vehicle being removed from the environment when reach the end of pause

        Returns
        -------
        end_trajectory : bool
            whether this vehicle reaches its end

        '''
       
        curr_speed = self.env.get_forward_speed(self.model_uniquename)
        vehicle_pos_2d = self.env.get_transform_2d(self.model_uniquename) # the (x,y) location and yaw angle of the vehicle
        self.speed.append(curr_speed)
        self.curr_speeds.append(curr_speed)
        
        # draw real trajectory if debug is enabled
        if self.debug_vehicle:
            self.vehicle_pose.append(vehicle_pos_2d[0])
            if len(self.vehicle_pose) == 2:
                self.env.draw_real_trajectory(self.vehicle_pose)
                
        # use pure-pursuit model to get the steer angle (in radius)
        delta, current_ref_speed, index, end_trajectory = self.pure_pursuit_control(vehicle_pos_2d, curr_speed, self.trajectory, self.ref_speed_list, self.index)
        self.index = index
        steer = np.clip(delta,-1.0,1.0)
        
        
        # If vehicle has safety distance set, check whether a vehicle is in the front
        current_ref_speed = self._obey_safety_distance(current_ref_speed)
        
        # If vehicle obey traffic lights and is going straight / turning left, check the traffic light state
        current_ref_speed = self._obey_traffic_light(current_ref_speed)
        
        #if self.debug_vehicle:
        #    print("current_ref_speed == ",current_ref_speed)
        
        self.ref_speeds.append(current_ref_speed)
        self.reference_speed.append(current_ref_speed)
        
        # get throttle to get the next reference speed 
        throttle = self.speed_control() # get the throttle control based on reference and current speed
        throttle = np.clip(throttle,0,1) # throttle value is [0,1]
        self.throttles.append(throttle) # for visualization
        
        # check whether we are reaching the destination or not
        # this part is different from the original version
        if end_trajectory and self.mode == "normal":
            vehicle_control = carla.VehicleControl(throttle = 0.0,steer=steer,brake = 1.0) # immediately stop the car
            self.env.apply_vehicle_control(self.model_uniquename, vehicle_control) # apply control to vehicle
            self.run = False
            self._destroy_vehicle()
            return end_trajectory
        elif end_trajectory and self.mode == "pause":
            vehicle_control = carla.VehicleControl(throttle = 0.0,steer=steer,brake = 1.0)
            self.env.apply_vehicle_control(self.model_uniquename, vehicle_control)
            return False
        
        
        
        # apply throttle-steer-brake control
        if curr_speed <= current_ref_speed:
            vehicle_control = carla.VehicleControl(throttle = throttle,steer=steer) 
        else:
            vehicle_control = carla.VehicleControl(throttle = throttle,steer=steer,brake = 0.5)
        self.env.apply_vehicle_control(self.model_uniquename, vehicle_control) # apply control to vehicle
        return end_trajectory            