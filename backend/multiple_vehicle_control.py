#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 09:54:39 2020

@author: shijiliu
"""


import carla
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time
import math

import control # the python-control package, install first

from intersection_definition import Intersection, get_traffic_lights
from carla_env import CARLA_ENV # self-written class that provides help functions, should be in the same folder
from configobj import ConfigObj

class VehicleControl(object):
    def __init__(self,env,vehicle_config, delta_seconds):
        '''
        

        Parameters
        ----------
        env : CARLA_ENV
            the self-written environment for simulation
        
        vehicle_config : ConfigObj
            the configuration file for this vehicle. The file is created inside the Intersection's add_vehicle function.
            containing the trajectory and speed reference for the vehicle. The configuration file should also indicate whether
            this vehicle should go or not.

        delta_seconds : float
            time between two adjacent simulation step. Used for creating discrete controller

        Returns
        -------
        None.

        '''
        
        self.env = env
        self.vehicle_config = vehicle_config
        self.model_uniquename = self.vehicle_config["uniquename"]
        self.command = self.vehicle_config["command"]
        self.trajectory = self.vehicle_config["trajectory"]
        self.ref_speed_list = self.vehicle_config["ref_speed_list"]
        self.obey_traffic_lights = self.vehicle_config["obey_traffic_lights"]
        self.run = self.vehicle_config["run"]
        self.safety_distance = self.vehicle_config["safety_distance"]
        
        # discrete step time
        self.delta_seconds = delta_seconds
        
        # PI controller constants
        self.KI = 0.02
        self.KP = 0.5
        
        # pure-pursuit model constants
        self.k = 0.1 # coefficient for look ahead
        self.Lfc = 4.0 # look ahead distance
        self.L = self.vehicle_config["bounding_box"].x#2.88 # wheelbase
        
        # essential storages for the controller to work
        self.init_values = deque(maxlen = 2) # the state space values of the system. For a control system to be fully functional
                                        # we need to give initial value
        self.ref_speeds = deque(maxlen = 2) # the reference / target speed
        self.curr_speeds = deque(maxlen = 2) # the measured speed of the vehicle
        
        # storage for the visualize the reference speed, throttle and measured speed.
        self.speed = []
        self.throttles = []
        self.reference_speed = []
    
        # give initial values to storage, assume the car is released at rest, with no initial speed or acceleration
        self.init_values.append(0) 
        self.ref_speeds.append(0)
        self.curr_speeds.append(0)
    
        self.current_ref_speed = 0
        self.index = 0
        
        
        
        
        # get the PI controller for the vehicle
        self._get_PI_controller()
        
        
        self.debug_vehicle = True # enable drawing vehicle trajectory
        self.vehicle_pose = deque(maxlen = 2)
        
        # indication of whether the vehicle stops at traffic light
        self.blocked_by_light = False
        
    def _get_PI_controller(self):
        '''
        Effects: create a discrete state-space PI controller
        '''
        num_pi = [self.KP, self.KI] # numerator of the PI transfer function (KP*s + KI)
        den_pi = [1.0, 0.01*self.KI/self.KP] # denominator of PI transfer function (s + 0.01*KI/KP)
    
        sys = control.tf(num_pi,den_pi) # get transfer function for PI controller (since the denominator has a small term 0.01*KI/KP, it is actually a lag-compensator)
        sys = control.sample_system(sys, self.delta_seconds) # discretize the transfer function (from s-domain which is continuous to z-domain)
                                                            #since our simulation is discrete
        sys = control.tf2ss(sys) # transform transfer function into state space.
        self.sys = sys  # the system is created for this vehicle
        
    def speed_control(self):
        '''
        Effects: get the reference speed, current (measured) speed and initial values
                 Use the difference 
                                   e = ref_speeds - curr_speeds 
                 as the input for the PI controller, derive the new throttle
    
        Parameters
        ----------
        self.sys : control.ss 
            state space controller 
        self.ref_speeds : list of float
            the desired speed we need
        self.curr_speeds : list of float
            the current speed
        self.init_values : the initial_values of the system
            DESCRIPTION.
    
        Returns
        -------
        throttle : float type
            DESCRIPTION.
    
        '''
        
        
        U0 = np.array(self.ref_speeds) - np.array(self.curr_speeds)
        #print(U0)
        _,y0,x0 = control.forced_response(self.sys,U = U0,X0 = self.init_values[0]) # y0 is the next values, x0 is the state evolution
                                                                          # see https://python-control.readthedocs.io/en/0.8.3/generated/control.forced_response.html#control.forced_response 
        self.init_values.append(x0[-1])
        throttle = y0[-1]
        return throttle
    
    def get_target_index(self,location_2d, current_forward_speed, trajectory):
        '''
        Get the target for the vehicle to navigate to
    
        Parameters
        ----------
        location_2d : (x,y)
            current location of the vehicle.
        current_forward_speed : float
            current speed of the vehicle.
        trajectory : numpy 2d array
            interpolated waypoints.
    
        Returns
        -------
        ind : TYPE
            DESCRIPTION.
        end_trajectory : TYPE
            DESCRIPTION.
    
        '''
        
        
        distance = np.sum((trajectory - location_2d)**2,axis = 1)**0.5
        ind = np.argmin(distance)
        l0 = 0.0
        
        Lf = self.k * current_forward_speed + self.Lfc
        
        while Lf > l0 and (ind + 1) < len(trajectory):
            delta_d = sum((trajectory[ind + 1] - trajectory[ind])**2)**0.5
            l0 += delta_d
            ind += 1
        
        if ind >= len(trajectory) - 1:
            end_trajectory = True
        else:
            end_trajectory = False
            
        return ind, end_trajectory
    
    def pure_pursuit_control(self,vehicle_pos_2d, current_forward_speed, trajectory, ref_speed_list, prev_index):
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
        
        current_ref_speed = ref_speed_list[index]
        
        return delta, current_ref_speed, index, end_trajectory
    
    def pure_pursuit_control_wrapper(self):
        '''
        Apply one step control to the vehicle, store essential information for further use

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
        #    print("--------")
        #    print("current_ref_speed == ",current_ref_speed)
        #    print("current_speed ==",curr_speed)
        
        self.ref_speeds.append(current_ref_speed)
        self.reference_speed.append(current_ref_speed)
        
        # get throttle to get the next reference speed 
        throttle = self.speed_control() # get the throttle control based on reference and current speed
        throttle = np.clip(throttle,0,1) # throttle value is [0,1]
        self.throttles.append(throttle) # for visualization
        
        # check whether we are reaching the destination or not
        if end_trajectory:
            vehicle_control = carla.VehicleControl(throttle = 0.0,steer=steer,brake = 1.0) # immediately stop the car
            self.env.apply_vehicle_control(self.model_uniquename, vehicle_control) # apply control to vehicle
            self.run = False
            self._destroy_vehicle()
            return end_trajectory
        
        # apply throttle-steer-brake control
        if curr_speed <= current_ref_speed:
            vehicle_control = carla.VehicleControl(throttle = throttle,steer=steer) 
        else:
            vehicle_control = carla.VehicleControl(throttle = throttle,steer=steer,brake = 0.5)
        self.env.apply_vehicle_control(self.model_uniquename, vehicle_control) # apply control to vehicle
        return end_trajectory
    
    
    def _obey_traffic_light(self, current_ref_speed):
        # the vehicle should take traffic lights into account when it is required 
        # to obey lights and is going straight or turning left
        self.blocked_by_light = False
        
        if not self.obey_traffic_lights:
            return current_ref_speed
        if self.command == "right":
            return current_ref_speed
        
        # check light state
        state = self.env.get_traffic_light_state(self.model_uniquename)
        
        if state == carla.TrafficLightState.Red or state == carla.TrafficLightState.Yellow:
            # add an indication that the vehicle is blocked by the traffic light
            self.blocked_by_light = True
            
            return 0.0 # stop the car immediately
        
        return current_ref_speed # obey light and light is green
    
    def _obey_safety_distance(self, current_ref_speed):
        
        has_vehicle_in_front, distance = self.env.check_vehicle_in_front(self.model_uniquename, self.safety_distance)
        if has_vehicle_in_front: 
            return 0.0
        
        return current_ref_speed
    
    def _destroy_vehicle(self):
        self.env.destroy_vehicle(self.model_uniquename)
    
def multiple_vehicle_control(env,intersection_list):
    vehicle_list = []
    while True:
        env.world.tick()
        
        # update the distance between vehicles after each tick
        env.update_vehicle_distance()
        
        for ii in range(len(intersection_list)-1,-1,-1):
            if intersection_list[ii].start_sim:
                for vehicle_config in intersection_list[ii].subject_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
                    
                for vehicle_config in intersection_list[ii].left_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
                    
                for vehicle_config in intersection_list[ii].right_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
        
                for vehicle_config in intersection_list[ii].ahead_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
                    vehicle_list.append(vehicle)
                    
                intersection_list.pop(ii)
        
        if len(vehicle_list) == 0:
            break
        
        '''
        Temp function. Start vehicle that's not running
        '''
        has_run = False
        for vehicle in vehicle_list:
            if vehicle.run:
                has_run = True
                break
        
        if not has_run:
            for vehicle in vehicle_list:
                vehicle.run = True
        
        for jj in range(len(vehicle_list) -1, -1, -1):
            vehicle = vehicle_list[jj]
            if vehicle.run:
                end_trajectory = vehicle.pure_pursuit_control_wrapper()
                if end_trajectory:
                    vehicle_list.pop(jj)
                    
def main():
    try:
        client = carla.Client("localhost",2000)
        client.set_timeout(10.0)
        world = client.load_world('Town05')
         
        # set the weather
        weather = carla.WeatherParameters(
            cloudiness=10.0,
            precipitation=0.0,
            sun_altitude_angle=90.0)
        world.set_weather(weather)
        
        # set the spectator position for demo purpose
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location(x=-133, y=1.29, z=75.0), carla.Rotation(pitch=-88.0, yaw= -1.85, roll=1.595))) # top view of intersection
        
        env = CARLA_ENV(world) 
        time.sleep(2) # sleep for 2 seconds, wait the initialization to finish
        
        traffic_light_list = get_traffic_lights(world.get_actors())
        
        intersection_list = []
        
        # intersection 1
        world_pos = (-133.0,0.0)#(25.4,0.0)
        
        intersection1 = Intersection(env, world_pos, traffic_light_list)
        intersection1.add_vehicle(obey_traffic_lights = False)
        
        intersection1.add_vehicle(command = "left", obey_traffic_lights = False)
        intersection1.add_vehicle(command = "right", obey_traffic_lights = False)
        
        intersection1.add_vehicle(gap = 5,choice = "left", obey_traffic_lights = False)
        intersection1.add_vehicle(gap = 5, choice = "left",command = "right", obey_traffic_lights = False)
        intersection1.add_vehicle(gap = 5,choice = "left",command = "left", obey_traffic_lights = False)
        intersection1.add_vehicle(choice = "right", obey_traffic_lights = False)
        intersection1.add_vehicle(choice = "right",command = "left", obey_traffic_lights = False)
        intersection1.add_vehicle(gap = 10.0,choice = "right",command = "right", obey_traffic_lights = False)
        intersection1.add_vehicle(choice = "ahead", obey_traffic_lights = False)
        intersection1.add_vehicle(choice = "ahead",command = "right", obey_traffic_lights = False)
        intersection1.add_vehicle(choice = "ahead",command = "left", obey_traffic_lights = False)
        
        intersection1._shift_vehicles(-10,index = 1)
        
        
        intersection1.start_sim = True
        
        intersection_list.append(intersection1)
        
        multiple_vehicle_control(env,intersection_list)
        
    finally:
        time.sleep(10)
        env.destroy_actors()                    

if __name__ == '__main__':
    main()