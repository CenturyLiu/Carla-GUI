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

from backend.initial_intersection import Init_Intersection, create_intersections, get_ego_spectator, get_ego_left_spectator, get_ego_driving_spectator
from backend.full_path_vehicle import LeadVehicleControl, FollowVehicleControl

from backend.intersection_settings_helper import write_intersection_settings, read_intersection_settings

from backend.human_ego_control import HumanEgoControlServer
    


def IntersectionBackend(env,intersection_list, allow_collision = True, spectator_mode = None, enable_human_control = False):
    
    '''
    back end function for the Intersection

    Parameters
    ----------
    spectator_mode : string, optional
        the spectator mode, valid value is "first_person" or "left". The default is None.

    allow_collision : bool, optional
        whether collision is allowed during simulation

    enable_human_control : bool, optional
        whether ego vehicle is controlled by human

    Returns
    -------
    None.

    '''
    
    vehicle_list = [] # list of "other" type vehicle
    started_intersection_list = []
    ego_vehicle_config = intersection_list[0].ego_vehicle #init_intersection.ego_vehicle
    lead_vehicle_config = intersection_list[0].lead_vehicle
    follow_vehicle_config = intersection_list[0].follow_vehicle
    
    spectator = env.world.get_spectator()
    
    # if enable_human_control, get the ego vehicle from the environment
    if enable_human_control:
        ego_vehicle_uniquename = ego_vehicle_config["uniquename"]
        human_control_server = HumanEgoControlServer() # create the server for receiving the human command
        spectator_mode = "human_driving"
    
    # assign the first full path vehicle, to determine whether 
    # each intersection should start
    if  lead_vehicle_config != None:
        first_full_path_vehicle_name = lead_vehicle_config["uniquename"]
        
        lead_vehicle = LeadVehicleControl(env,lead_vehicle_config,env.delta_seconds,allow_collision)
        ego_vehicle = FollowVehicleControl(env, ego_vehicle_config, env.delta_seconds,allow_collision)
        end_lead = False
        ego_vehicle.use_distance_mode(ego_vehicle_config["lead_distance"]) #use distance control mode with lead_distance
        
    else:
        first_full_path_vehicle_name = ego_vehicle_config["uniquename"]
        ego_vehicle = FollowVehicleControl(env, ego_vehicle_config, env.delta_seconds,allow_collision)
        end_lead = True
        ego_vehicle.use_speed_mode()
    
    # assign the vehicle for the spectator to follow
    if follow_vehicle_config != None:
        spectator_vehicle = follow_vehicle_config
        spectator_bb = follow_vehicle_config["bounding_box"]
        follow_vehicle = FollowVehicleControl(env, follow_vehicle_config, env.delta_seconds,allow_collision)
        end_follow = False
        follow_vehicle.use_distance_mode(ego_vehicle_config["follow_distance"])
    else:
        spectator_vehicle = ego_vehicle_config
        spectator_bb = ego_vehicle_config["bounding_box"]
        end_follow = True
    
    if enable_human_control:
        spectator_bb = ego_vehicle_config["bounding_box"]
    
        
    
    end_ego = False
    # get the init intersection
    init_intersection = intersection_list.pop(0)
    started_intersection_list.append(init_intersection)
    
    for vehicle_config in init_intersection.subject_vehicle:
        # initialize vehicles by different type (ego,lead,follow,other)
        if vehicle_config["vehicle_type"] == "other":
            vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
            vehicle_list.append(vehicle)
    
    for vehicle_config in init_intersection.left_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
        vehicle_list.append(vehicle)
                    
    for vehicle_config in init_intersection.right_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
        vehicle_list.append(vehicle)
        
    for vehicle_config in init_intersection.ahead_vehicle:
        vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
        vehicle_list.append(vehicle)
    
    

    ego_uniquename = ego_vehicle_config["uniquename"]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file = open("../data_collection/Urb" + timestr + ".txt", "w+" )
    world_snapshot = env.world.get_snapshot()
    tm = world_snapshot.timestamp
    file.write("the experiment starts from " + str(tm.elapsed_seconds) + "(seconds)\n")
    print("start urban recordings: ")
    
    while True:
        world_snapshot = env.world.get_snapshot()
        ego_id = (int)(ego_uniquename.split("_")[1])
        ego_actor = world_snapshot.find(ego_id)

        world_snapshot = env.world.get_snapshot()
        tm = world_snapshot.timestamp

        file.write("time: " + str(tm.elapsed_seconds)+"(seconds)\n")
        ego_actor_transform = ego_actor.get_transform()
        file.write("location: " + str(ego_actor_transform.location) + "(meters)\n" )
        ego_actor_velocity = ego_actor.get_velocity()
        file.write("Rotation: " + str(ego_actor_velocity) + "(degrees)\n")
        ego_actor_angular_velocity = ego_actor.get_angular_velocity()
        file.write("Angular velocity: " + str(ego_actor.get_angular_velocity()) + "(rad/s)\n")
        ego_actor_acceleration = ego_actor.get_acceleration()
        file.write("Acceleration: " + str(ego_actor.get_acceleration()) + "(m/s2)\n")

        env.world.tick()
        # update the distance between vehicles after each tick
        env.update_vehicle_distance()
        
        # update the ego spectator
        if env.vehicle_available(spectator_vehicle["uniquename"]):
            spectator_vehicle_transform = env.get_transform_3d(spectator_vehicle["uniquename"])
            #spectator_transform = get_ego_spectator(spectator_vehicle_transform,distance = -10)
            if spectator_mode == "first_person":
                spectator_transform = get_ego_spectator(spectator_vehicle_transform, distance = -10)
                spectator.set_transform(spectator_transform)
            elif spectator_mode == "left":
                if env.vehicle_available(ego_vehicle_config["uniquename"]):
                    spectator_vehicle_transform = env.get_transform_3d(ego_vehicle_config["uniquename"])
                    spectator_transform = get_ego_left_spectator(spectator_vehicle_transform)
                    spectator.set_transform(spectator_transform)
            elif spectator_mode == "human_driving":
                if env.vehicle_available(ego_vehicle_config["uniquename"]):
                    spectator_vehicle_transform = env.get_transform_3d(ego_vehicle_config["uniquename"])
                    #spectator_vehicle_transform = env.get_transform_3d(ego_vehicle_uniquename)
                    spectator_transform = get_ego_driving_spectator( spectator_vehicle_transform, spectator_bb)
                    spectator.set_transform(spectator_transform)
        #else:
        #    spectator_transform = carla.Transform(carla.Location(x= 25.4, y=1.29, z=75.0), carla.Rotation(pitch=-88.0, yaw= -1.85, roll=1.595))
        #spectator.set_transform(spectator_transform)
        
        
        for ii in range(len(intersection_list)-1,-1,-1):
            # check whether the intersection should start
            intersection_list[ii].start_simulation(first_full_path_vehicle_name)
            if intersection_list[ii].start_sim:
                for vehicle_config in intersection_list[ii].subject_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
                    vehicle_list.append(vehicle)
                    
                for vehicle_config in intersection_list[ii].left_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
                    vehicle_list.append(vehicle)
                    
                for vehicle_config in intersection_list[ii].right_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
                    vehicle_list.append(vehicle)
        
                for vehicle_config in intersection_list[ii].ahead_vehicle:
                    vehicle = VehicleControl(env, vehicle_config, env.delta_seconds,allow_collision)
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
            if not enable_human_control:
                # use the automatic control provided by the back-end, which is set as default
                end_ego = ego_vehicle.pure_pursuit_control_wrapper()
                ego_stop_at_light = ego_vehicle.blocked_by_light
            else:
                # get control from human
                human_command = human_control_server.get_human_command()
                # format the command into carla.VehicleControl
                ego_vehicle_control = carla.VehicleControl(throttle = human_command[0] ,steer=human_command[1],brake = human_command[2])
                # apply control to the vehicle
                env.apply_vehicle_control(ego_vehicle_uniquename , ego_vehicle_control)
                
                
                end_ego = ego_vehicle.fake_pure_pursuit_control_wrapper() # change all internal settings as the real wrapper, but 
                                                                          # don't apply control to vehicle
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
        
        intersection_list = create_intersections(env, 4, traffic_light_list, navigation_speed = 30.0)
        init_intersection = intersection_list[0]
        normal_intersections = intersection_list[1:]
        init_intersection.add_ego_vehicle(safety_distance = 15.0, stop_choice = "abrupt", vehicle_color = '255,255,255')
        init_intersection.add_follow_vehicle(follow_distance = 20.0, stop_choice = "penetrate", penetrate_distance = 2.0)
        init_intersection.add_lead_vehicle(lead_distance = 20.0, stop_choice = "abrupt", vehicle_color = '255,255,255')
        init_intersection.add_vehicle(choice = "left", stop_choice = "abrupt", vehicle_color = '255,255,255')
        init_intersection.add_vehicle(choice = "right",command="left")
        
        # test edit settings
        name1 = init_intersection.add_vehicle(choice = "ahead",command="left")
        name2 = init_intersection.add_vehicle(choice = "ahead",command = "right")
        
        name1 = init_intersection.edit_vehicle_settings(name1, choice = "ahead", vehicle_color = '128,128,128')
        name2 = init_intersection.edit_vehicle_settings(name2, choice = "ahead", gap = 15.0, vehicle_color = '128,128,128')
        
        vehicle_settings_entered = init_intersection.get_vehicle_settings(name2)
        print(vehicle_settings_entered["gap"])
        
        #init_intersection.edit_traffic_light("subject")
        #init_intersection.edit_traffic_light("left",red_start = 40.0,red_end = 60.0,yellow_start=30.0,yellow_end=40.0,green_start=0.0,green_end = 30.0)
        #init_intersection.edit_traffic_light("right",red_start = 0.0,red_end = 10.0,yellow_start=10.0,yellow_end=20.0,green_start=20.0,green_end = 40.0)
        #init_intersection.edit_traffic_light("ahead",red_start = 20.0,red_end = 40.0,yellow_start=10.0,yellow_end=20.0,green_start=0.0,green_end = 10.0)
        
        # get bounding box
        bb = init_intersection.get_vehicle_bounding_box(name1)
        print("bb.x = %f, bb.y = %f, bb.z = %f" % (bb.x, bb.y, bb.z))
        
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
        
        
        
        
        IntersectionBackend(env,intersection_list,allow_collision = False)
    finally:
        time.sleep(10)
        env.destroy_actors()
        
if __name__ == '__main__':
    main()