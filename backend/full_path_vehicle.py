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
            self._display_vehicle_type()
                
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
    

class FollowVehicleControl(VehicleControl):
    # the FollowVehicle class is created for both ego and follow vehicle
    # this kind of vehicle has 2 modes:
    #    - speed control mode, when the vehicle is not following another vehicle
    #    - distance control mode, when the vehicle is following another vehicle
    
    def __init__(self,env,vehicle_config, delta_seconds):
        super().__init__(env, vehicle_config, delta_seconds)
        
        # control mode
        self.mode = "speed"
        
    def _get_distance_controller(self,delta_seconds):
        '''
        Effects: create distance controller
        '''
        KP_1 = 0.5#1.0
        KI_1 = 0.5#1.0
        
        num_pi = [-KP_1, -KI_1] # numerator of the PI transfer function (KP*s + KI)
        den_pi = [1.0, 0.01*KI_1/KP_1] # denominator of PI transfer function (s + 0.01*KI/KP)
    
        sys = control.tf(num_pi,den_pi) # get transfer function for PI controller (since the denominator has a small term 0.01*KI/KP, it is actually a lag-compensator)
        sys = control.sample_system(sys, delta_seconds) # discretize the transfer function (from s-domain which is continuous to z-domain)
                                                            #since our simulation is discrete
        sys = control.tf2ss(sys) # transform transfer function into state space.
        
        
        self.distance_sys = sys
        
    def _get_distance_control_reference_speed(self):
        '''
        
    
        Parameters
        ----------
        self.distance_sys : control.ss 
            state space controller.
        self.ref_distance : deque(maxlen=2), float
            the reference distance.
        self.curr_distance : deque(maxlen=2), float
            current distance between two vehicles.
        init_values : the initial_values of the system
    
        Returns
        -------
        None.
    
        '''
        U0 = np.array(self.ref_distance) - np.array(self.curr_distance)
        #print(U0)
        _,y0,x0 = control.forced_response(self.distance_sys,U = U0,X0 = self.distance_init_values[0]) # y0 is the next values, x0 is the state evolution
                                                                          # see https://python-control.readthedocs.io/en/0.8.3/generated/control.forced_response.html#control.forced_response 
        self.distance_init_values.append(x0[-1])
        ref_speed = y0[-1]
        
        #print(ref_speed)
        
        return ref_speed
    
    
    def use_distance_mode(self, follow_distance):
        # change the mode
        self.mode = "distance"
        
        # store the follow_distance
        self.follow_distance = follow_distance + self.L # self.L is the length of the bounding box
        
        # storage for distance controller
        self.distance_init_values = deque(maxlen = 2)
        self.ref_distance = deque(maxlen = 2)
        self.curr_distance = deque(maxlen = 2)
        
        # initialize those storage
        self.distance_init_values.append(0)
        self.ref_distance.append(self.follow_distance)
        self.curr_distance.append(self.follow_distance)
        
        # get the controller for distance control
        self._get_distance_controller(self.env.delta_seconds)
        
    def use_speed_mode(self):
        self.mode = "speed"
        
    def get_current_distance(self, target_transform):
        '''
        get the real distance between the vehicle and the one it is following

        Parameters
        ----------
        target_transform : carla.Transform
            the transformation of the target.

        Returns
        -------
        None.

        '''
        # distance control seems problematic, temporarily still keep using speed control
        self.mode = "speed"#"distance"
        
        target_location = target_transform.location
        # get the local transformation
        local_transform = self.env.get_transform_3d(self.model_uniquename)
        local_location = local_transform.location
        forward_vector = local_transform.get_forward_vector()
        forward_vector_2d = np.array([forward_vector.x,forward_vector.y])
        unit_forward_vector_2d =  forward_vector_2d / np.linalg.norm(forward_vector_2d)
        
        vec_loc_target = np.array([target_location.x - local_location.x,target_location.y - local_location.y])
        
        # get the distance in the direction of local vehicle heading
        distance = np.dot(vec_loc_target,unit_forward_vector_2d)
        
        #print(distance)
        
        self.ref_distance.append(self.follow_distance)
        self.curr_distance.append(distance)
        
    
    def pure_pursuit_control(self,vehicle_pos_2d, current_forward_speed, trajectory, ref_speed_list, prev_index):
        
        # override the pure_pursuit_control method
        # use self.mode to decide how we are going to 
        # assign the model reference speed
        
        '''
        
    
        Parameters
        ----------
        vehicle_pos_2d : (location_2d,yaw)
            tuple of vehicle location and heading in 2d.
            location_2d : (x,y), both x and y are in meter
            yaw : heading angle **Note** yaw is in degree
        current_forward_speed : float
            the current velocity of the vehicle.
        trajectory : numpy 2d array
            interpolated waypoints.
        ref_speed_list : list
            the reference speed corresponding to each way point
        prev_index : int
            the previous index
        Returns
        -------
        delta : float
            steer angle of the vehicle.
        current_ref_speed : the reference speed
            DESCRIPTION.
        index : int
            the index of the target.
        end_trajectory : boolean
            whether we have reached clos enough to the destination.
    
        '''
        
        
        
        location_2d, yaw = vehicle_pos_2d
        yaw = np.deg2rad(yaw) # change the unit the radius
        index, end_trajectory = self.get_target_index(location_2d, current_forward_speed, trajectory)
        
        if prev_index >= index:
            index = prev_index
            
        if index < len(trajectory):
            tx = trajectory[index][0]
            ty = trajectory[index][1]
        else:
            tx = trajectory[-1][0]
            ty = trajectory[-1][1] 
        
        alpha = math.atan2(ty - location_2d[1],tx - location_2d[0]) - yaw
        
        if current_forward_speed < 0: #back, should not happen in our case
            alpha = math.pi - alpha
        
        Lf = self.k * current_forward_speed + self.Lfc
        
        delta = math.atan2(2.0 * self.L * math.sin(alpha) / Lf, 1.0)
        #print("delta == ", delta, "yaw == ", yaw)
        
        if self.mode == "speed":
            current_ref_speed = ref_speed_list[index]
        elif self.mode == "distance":
            current_ref_speed = self._get_distance_control_reference_speed() 
        
        return delta, current_ref_speed, index, end_trajectory