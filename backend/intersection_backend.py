#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:20:00 2020

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

from backend.generate_path_omit_regulation import generate_path
from backend.intersection_definition import Intersection, get_traffic_lights, get_trajectory, smooth_trajectory
from backend.carla_env import CARLA_ENV # self-written class that provides help functions, should be in the same folder
from configobj import ConfigObj
from backend.multiple_vehicle_control import VehicleControl

import copy

from backend.initial_intersection import Init_Intersection, create_intersections, get_ego_spectator, get_ego_left_spectator
from backend.full_path_vehicle import LeadVehicleControl, FollowVehicleControl

from backend.intersection_settings_helper import write_intersection_settings, read_intersection_settings

    


def IntersectionBackend(env,intersection_list):
    vehicle_list = [] # list of "other" type vehicle
    started_intersection_list = []
    ego_vehicle_config = intersection_list[0].ego_vehicle #init_intersection.ego_vehicle
    lead_vehicle_config = intersection_list[0].lead_vehicle
    follow_vehicle_config = intersection_list[0].follow_vehicle
    
    spectator = env.world.get_spectator()
    
    # assign the first full path vehicle, to determine whether 
    # each intersection should start
    if  lead_vehicle_config != None:
        first_full_path_vehicle_name = lead_vehicle_config["uniquename"]
        
        lead_vehicle = LeadVehicleControl(env,lead_vehicle_config,env.delta_seconds)
        ego_vehicle = FollowVehicleControl(env, ego_vehicle_config, env.delta_seconds)
        end_lead = False
        ego_vehicle.use_distance_mode(ego_vehicle_config["lead_distance"]) #use distance control mode with lead_distance
        
    else:
        first_full_path_vehicle_name = ego_vehicle_config["uniquename"]
        ego_vehicle = FollowVehicleControl(env, ego_vehicle_config, env.delta_seconds)
        end_lead = True
        ego_vehicle.use_speed_mode()
    
    # assign the vehicle for the spectator to follow
    if follow_vehicle_config != None:
        spectator_vehicle = follow_vehicle_config
        follow_vehicle = FollowVehicleControl(env, follow_vehicle_config, env.delta_seconds)
        end_follow = False
        follow_vehicle.use_distance_mode(ego_vehicle_config["follow_distance"])
    else:
        spectator_vehicle = ego_vehicle_config
        end_follow = True
    
    end_ego = False
    # get the init intersection
    init_intersection = intersection_list.pop(0)
    started_intersection_list.append(init_intersection)
    
    for vehicle_config in init_intersection.subject_vehicle:
        # initialize vehicles by different type (ego,lead,follow,other)
        if vehicle_config["vehicle_type"] == "other":
            vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
            vehicle_list.append(vehicle)
    
    for vehicle_config in init_intersection.left_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
        vehicle_list.append(vehicle)
                    
    for vehicle_config in init_intersection.right_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
        vehicle_list.append(vehicle)
        
    for vehicle_config in init_intersection.ahead_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds)
        vehicle_list.append(vehicle)
    
    
    while True:
        env.world.tick()
        
        # update the distance between vehicles after each tick
        env.update_vehicle_distance()
        
        # update the ego spectator
        '''
        if env.vehicle_available(spectator_vehicle["uniquename"]):
            spectator_vehicle_transform = env.get_transform_3d(spectator_vehicle["uniquename"])
            #spectator_transform = get_ego_spectator(spectator_vehicle_transform,distance = -10)
            spectator_transform = get_ego_left_spectator(spectator_vehicle_transform)
            spectator.set_transform(spectator_transform)
        '''
        #else:
        #    spectator_transform = carla.Transform(carla.Location(x= 25.4, y=1.29, z=75.0), carla.Rotation(pitch=-88.0, yaw= -1.85, roll=1.595))
        #spectator.set_transform(spectator_transform)
        
        
        for ii in range(len(intersection_list)-1,-1,-1):
            # check whether the intersection should start
            intersection_list[ii].start_simulation(first_full_path_vehicle_name)
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
                
                # move the intersection to started intersection list
                intersection = intersection_list.pop(ii)
                started_intersection_list.append(intersection)
                
        ego_stop_at_light = False        
        
        # set the traffic lights based on traffic light setting
        for started_intsection in started_intersection_list:
            started_intsection.set_intersection_traffic_lights()
        
        # check the current location of the lead vehicle and ego vehicle if they are available
        # so as to update the curr_distance for ego, and follow vehicle
        lead_transform = None
        ego_transform = None
        if not end_lead:
            lead_transform = lead_vehicle.get_vehicle_transform()
            
        if not end_ego:
            ego_transform = ego_vehicle.get_vehicle_transform()
            if lead_transform != None:
                ego_vehicle.get_current_distance(lead_transform)
            else:
                ego_vehicle.use_speed_mode() # no lead available, change to speed control
            
        if not end_follow:
            if ego_transform != None:
                follow_vehicle.get_current_distance(ego_transform)
            else:
                follow_vehicle.use_speed_mode()# no ego available, change to speed control
        
        
        
        
        # apply control to ego vehicle, get whether it stops at traffic light
        if not end_ego:        
            end_ego = ego_vehicle.pure_pursuit_control_wrapper()
            ego_stop_at_light = ego_vehicle.blocked_by_light
        
        # apply control to lead vehicle
        if not end_lead:
            if ego_stop_at_light and lead_vehicle.mode != "pause" : # lead is still in full path mode when ego stops
                lead_vehicle.change_mode("pause")
            elif not ego_stop_at_light and lead_vehicle.mode == "pause":
                lead_vehicle.change_mode("normal")
                
            end_lead = lead_vehicle.pure_pursuit_control_wrapper()
            
        # apply control to follow vehicle    
        if not end_follow:
            end_follow = follow_vehicle.pure_pursuit_control_wrapper()
                
            
        
        
                
        if len(vehicle_list) == 0 and end_lead and end_ego and end_follow: # all vehicle has stopped
            break        
                
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
        spectator.set_transform(carla.Transform(carla.Location(x=-190, y=1.29, z=75.0), carla.Rotation(pitch=-88.0, yaw= -1.85, roll=1.595))) # top view of intersection
        
        env = CARLA_ENV(world) 
        time.sleep(2) # sleep for 2 seconds, wait the initialization to finish
        
        traffic_light_list = get_traffic_lights(world.get_actors())
        
        intersection_list = create_intersections(env, 4, traffic_light_list)
        init_intersection = intersection_list[0]
        normal_intersections = intersection_list[1:]
        init_intersection.add_ego_vehicle(safety_distance = 15.0, stop_choice = "abrupt", vehicle_color = '255,255,255')
        init_intersection.add_follow_vehicle(follow_distance = 20.0, stop_choice = "penetrate", penetrate_distance = 2.0)
        init_intersection.add_lead_vehicle(lead_distance = 20.0, stop_choice = "abrupt")
        init_intersection.add_vehicle(choice = "left", stop_choice = "abrupt", vehicle_color = '255,255,255')
        init_intersection.add_vehicle(choice = "right",command="left")
        init_intersection.add_vehicle(choice = "ahead",command="left")
        init_intersection.add_vehicle(choice = "ahead",command = "right")
        #init_intersection.edit_traffic_light("subject")
        #init_intersection.edit_traffic_light("left",red_start = 40.0,red_end = 60.0,yellow_start=30.0,yellow_end=40.0,green_start=0.0,green_end = 30.0)
        #init_intersection.edit_traffic_light("right",red_start = 0.0,red_end = 10.0,yellow_start=10.0,yellow_end=20.0,green_start=20.0,green_end = 40.0)
        #init_intersection.edit_traffic_light("ahead",red_start = 20.0,red_end = 40.0,yellow_start=10.0,yellow_end=20.0,green_start=0.0,green_end = 10.0)
        
        
        intersection_list[1].add_vehicle(choice = "ahead")
        intersection_list[1].add_vehicle(choice = "left",command="left")
        intersection_list[1].add_vehicle(choice = "right",command = "left")
        intersection_list[1].add_vehicle(choice = "right",command = "right")
        intersection_list[1]._shift_vehicles(-10, choice = "right",index = 0)
        #intersection_list[1].edit_traffic_light("left")
        
        intersection_list[2].add_vehicle(choice = "ahead")
        intersection_list[2].add_vehicle(choice = "left",command="left")
        intersection_list[2].add_vehicle(choice = "right",command = "left")
        intersection_list[2].add_vehicle(choice = "right",command = "right")
        #intersection_list[2].edit_traffic_light("right")
        
        intersection_list[3].add_vehicle(command = "left")
        intersection_list[3].add_vehicle()
        #intersection_list[3].edit_traffic_light("ahead")
        
        # test import/export
        init_setting = init_intersection.export_settings()
        
        intersection_list[3].import_settings(init_setting)
        intersection_list[3].add_vehicle(command = "left")
        intersection_list[3].add_vehicle()
        third_setting = intersection_list[3].export_settings()
        
        write_intersection_settings("third_intersection_setting",third_setting)
        new_third_setting = read_intersection_settings('third_intersection_setting')
        
        intersection_list[2].import_settings(new_third_setting)
        
        
        
        
        IntersectionBackend(env,intersection_list)
    finally:
        time.sleep(10)
        env.destroy_actors()
        
if __name__ == '__main__':
    main()