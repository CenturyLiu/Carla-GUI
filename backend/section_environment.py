#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:20:28 2020

@author: shijiliu
"""

# define a class for creating the simulation environment for the section

import sys
sys.path.append("..")

import carla
from backend.carla_env import CARLA_ENV 
import math
import time
import numpy as np
from configobj import ConfigObj
import copy
from backend.section_definition import Section
from backend.section_init_definition import InitSection
from backend.generate_path_omit_regulation import generate_path
from backend.intersection_definition import smooth_trajectory, get_trajectory
from backend.multiple_vehicle_control import VehicleControl
from backend.multiple_vehicle_control_debug import VehicleControl_debug
from backend.initial_intersection import get_ego_spectator, get_ego_left_spectator
from backend.section_vehicle_control import FullPathVehicleControl

# color for debug use
red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)


class FreewayEnv(object):
    # this class holds all methods related to create a simulation environment for freeway
    def __init__(self, env, number_of_sections, max_speed = 30.0):
        '''
        initialize the freeway simulation environment

        Parameters
        ----------
        number_of_sections : int
            number of sections for the freeway environment.

        max_speed : float
            the max speed of vehicle. Default to be 30.0. Vehicle will go at 75% of its max speed when
            under speed control mode
            
        Returns
        -------
        None

        '''
        # debug 
        self.DEBUG_TRAJECTORY = True
        self.DEBUG_SUBJECTPOINTS = True
        self.DEBUG_SECTION = True
        
        # store the number of sections
        self.number_of_sections = number_of_sections
        
        self.env = env
        
        self.spectator = self.env.world.get_spectator()
        
        
        
        self.carla_map = self.env.world.get_map()
        
        # get the subject waypoint of each section
        self.subject_point_list = self._get_section_subject_points((320,13.75))
        
        # store the reference speed
        self.max_speed = max_speed
        self.navigation_speed = self.max_speed * 0.75
        
        # create the simulation environment and generate the trajectory
        self._create_simulation_env()
        
        # give the trajectory and reference speed list to the initial intersection
        self.section_list[0].get_full_path_trajectory(self.smoothed_full_trajectory, self.ref_speed_list, self.left_smoothed_full_trajectory, self.left_ref_speed_list)
    
        
    
    
    #def __del__(self):
    #    self.env.destroy_actors()
    
    # public methods
    def get_section_list(self):
        return self.section_list
    
    def SectionBackend(self):
        '''
        back end function for the freeway

        Returns
        -------
        None.

        '''
        init_section = self.section_list[0]
        ego_vehicle =  VehicleControl(self.env, init_section.ego_vehicle, self.env.delta_seconds)
        ego_uniquename = init_section.ego_vehicle["uniquename"]
        left_follow_vehicle = []
        subject_follow_vehicle = []
        left_lead_vehicle = []
        subject_lead_vehicle = []
        
        # check whether ego vehicle comes to destination
        ego_end = False
        
        # create vehicle control object
        for vehicle_config in init_section.left_follow_vehicle:
            left_follow_vehicle.append(FullPathVehicleControl(self.env, vehicle_config, self.env.delta_seconds))
            
        for vehicle_config in init_section.subject_follow_vehicle:
            subject_follow_vehicle.append(FullPathVehicleControl(self.env, vehicle_config, self.env.delta_seconds))
            
        for vehicle_config in init_section.left_lead_vehicle:
            left_lead_vehicle.append(FullPathVehicleControl(self.env, vehicle_config, self.env.delta_seconds))
            
        for vehicle_config in init_section.subject_lead_vehicle:
            subject_lead_vehicle.append(FullPathVehicleControl(self.env, vehicle_config, self.env.delta_seconds))
            
        
        # store the current section that is functioning
        curr_section = init_section
        self.section_list.pop(0)
        
        # main loop for control    
        while True:
            self.env.world.tick()
            
            # update the distance between vehicles after each tick
            self.env.update_vehicle_distance()
            
            # change spectator view
            '''
            if self.env.vehicle_available(ego_uniquename):
                 spectator_vehicle_transform = self.env.get_transform_3d(ego_uniquename)
                 spectator_transform = get_ego_spectator(spectator_vehicle_transform,distance = -40)
                 self.spectator.set_transform(spectator_transform)
            '''
            # section based control
            # update the elapsed time of the current section
            local_time = curr_section.tick()
            
            for vehicle in left_follow_vehicle:
                vehicle.update_local_time(local_time)
                
            for vehicle in subject_follow_vehicle:
                vehicle.update_local_time(local_time)
                
            for vehicle in left_lead_vehicle:
                vehicle.update_local_time(local_time)
            
            for vehicle in subject_lead_vehicle:
                vehicle.update_local_time(local_time)
            
            # apply section control, implement later
            
            
                
            # apply control to vehicles
            if not ego_end:
                ego_end = ego_vehicle.pure_pursuit_control_wrapper()
            
            '''
            print("--------")
            print("len(left_follow_vehicle) == ", len(left_follow_vehicle))
            print("len(subject_follow_vehicle) == ", len(subject_follow_vehicle))
            print("len(left_lead_vehicle) == ", len(left_lead_vehicle))
            print("len(subject_lead_vehicle) == ", len(subject_lead_vehicle))
            '''
            
            for jj in range(len(left_follow_vehicle) - 1,-1,-1):
                vehicle = left_follow_vehicle[jj]
                end_trajectory = vehicle.pure_pursuit_control_wrapper()
                if end_trajectory:
                    left_follow_vehicle.pop(jj)
                    
            for jj in range(len(subject_follow_vehicle) - 1,-1,-1):
                vehicle = subject_follow_vehicle[jj]
                end_trajectory = vehicle.pure_pursuit_control_wrapper()
                if end_trajectory:
                    subject_follow_vehicle.pop(jj)
                    
            for jj in range(len(left_lead_vehicle) - 1,-1,-1):
                vehicle = left_lead_vehicle[jj]
                end_trajectory = vehicle.pure_pursuit_control_wrapper()
                if end_trajectory:
                    left_lead_vehicle.pop(jj)
                    
            for jj in range(len(subject_lead_vehicle) - 1,-1,-1):
                vehicle = subject_lead_vehicle[jj]
                end_trajectory = vehicle.pure_pursuit_control_wrapper()
                if end_trajectory:
                    subject_lead_vehicle.pop(jj)
            
            if ego_end and len(left_follow_vehicle) == 0 and len(subject_follow_vehicle) == 0 and len(left_lead_vehicle) == 0 and len(subject_lead_vehicle) == 0:
                # exit simulation when all vehicles have arrived at their destination
                break
                
            
            # check whether the subject vehicle is in the next section, if that's the case, change the curr_section
            # implement later
        
    
    # private methods
    def _create_simulation_env(self):
        # create the freeway environment
        # this function is the counterpart of the "create_intersections" 
        # function for intersection backend
        
        self.section_list = [] # list for all sections 
        self.trajectory_ref_point_list = [] # list for full path trajectory waypoints
        
        initial_section = InitSection(self.env, self.subject_point_list[0]) # create the initial intersection
        self.section_list.append(initial_section) 
        self.trajectory_ref_point_list += initial_section.get_section_trajectory_points()
        
        if self.DEBUG_SECTION:
            trajectory_pt = initial_section.get_section_trajectory_points()
            for pt in trajectory_pt:
                loc1 = pt.transform.location
                self.env.world.debug.draw_point(loc1, size = 0.05, color = red, life_time=0.0, persistent_lines=True)
                
        
        for ii in range(1, self.number_of_sections):
            normal_section = Section(self.env, self.subject_point_list[ii])
            self.section_list.append(normal_section)
            self.trajectory_ref_point_list += normal_section.get_section_trajectory_points()
            if self.DEBUG_SECTION:
                trajectory_pt = normal_section.get_section_trajectory_points()
                for pt in trajectory_pt:
                    loc1 = pt.transform.location
                    self.env.world.debug.draw_point(loc1, size = 0.05, color = red, life_time=0.0, persistent_lines=True)
                    
            
        if self.DEBUG_SUBJECTPOINTS:
            color = green
            for ii in range(len(self.subject_point_list)):
                loc1 = self.subject_point_list[ii].transform.location
                self.env.world.debug.draw_point(loc1, size = 0.1, color = color, life_time=0.0, persistent_lines=True)
        
        
        # connect all reference points for all sections
        full_trajectory = generate_path(self.env, self.trajectory_ref_point_list[0] , self.trajectory_ref_point_list[1], waypoint_separation = 4)
        for ii in range(1, len(self.trajectory_ref_point_list) - 1):
            trajectory = generate_path(self.env, self.trajectory_ref_point_list[ii] , self.trajectory_ref_point_list[ii + 1], waypoint_separation = 4)
            full_trajectory += trajectory[1:]
            
        self.section_subject_trajectory = full_trajectory
        '''
        full_trajectory = []
        for pt in self.trajectory_ref_point_list:
            location = pt.transform.location
            full_trajectory.append((location.x,location.y))
        '''
        
        # create smoothed trajectory and reference speed list
        whole_trajectory = [((pt[0],pt[1]),self.navigation_speed) for pt in full_trajectory]
        
        smoothed_full_trajectory, ref_speed_list = get_trajectory(whole_trajectory)
        self.smoothed_full_trajectory = smoothed_full_trajectory
        self.ref_speed_list = ref_speed_list
        
        if self.DEBUG_TRAJECTORY:
            color = cyan
            for ii in range(1,len(smoothed_full_trajectory)):
                loc1 = carla.Location(x = smoothed_full_trajectory[ii - 1][0], y = smoothed_full_trajectory[ii - 1][1], z = 10.0)
                loc2 = carla.Location(x = smoothed_full_trajectory[ii][0], y = smoothed_full_trajectory[ii][1], z = 10.0)
                self.env.world.debug.draw_arrow(loc1, loc2, thickness = 0.05, arrow_size = 0.1, color = color, life_time=0.0, persistent_lines=True)
    
    
        # get the trajectory for the left lane
        self.left_lane_waypoints_list = []
        for waypoint in self.trajectory_ref_point_list:
            left_waypoint = self._get_left_waypoint(waypoint)
            self.left_lane_waypoints_list.append(left_waypoint)
            
        if self.DEBUG_SECTION:
            for ii in range(1,len(self.left_lane_waypoints_list)):
                loc1 = self.left_lane_waypoints_list[ii - 1].transform.location
                loc2 = self.left_lane_waypoints_list[ii].transform.location
                self.env.world.debug.draw_arrow(loc1, loc2, thickness = 0.1, arrow_size = 0.2, color = cyan, life_time=0.0, persistent_lines=True)
        
        
        left_full_trajectory = []
        for pt in self.left_lane_waypoints_list:
            location = pt.transform.location
            left_full_trajectory.append((location.x,location.y))
        
        
        left_whole_trajectory = [((pt[0],pt[1]),self.navigation_speed) for pt in left_full_trajectory]
        
        left_smoothed_full_trajectory, left_ref_speed_list = get_trajectory(left_whole_trajectory)
        self.left_smoothed_full_trajectory = left_smoothed_full_trajectory
        self.left_ref_speed_list = left_ref_speed_list
        
        if self.DEBUG_TRAJECTORY:
            color = blue
            for ii in range(1,len(left_smoothed_full_trajectory)):
                loc1 = carla.Location(x = left_smoothed_full_trajectory[ii - 1][0], y = left_smoothed_full_trajectory[ii - 1][1], z = 10.0)
                loc2 = carla.Location(x = left_smoothed_full_trajectory[ii][0], y = left_smoothed_full_trajectory[ii][1], z = 10.0)
                self.env.world.debug.draw_arrow(loc1, loc2, thickness = 0.05, arrow_size = 0.1, color = color, life_time=0.0, persistent_lines=True)
        
            
        
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
    
    def _get_section_subject_points(self, initial_point):
        # get the section subject points
        
        world_pose_list = []
        
        initial_point_raw = carla.Location(initial_point[0], initial_point[1], z = 10.0)
        initial_way_point = self.carla_map.get_waypoint(initial_point_raw)
        
        world_pose_list.append(initial_way_point)
        
        curr_waypoint = initial_way_point
        
        for ii in range(self.number_of_sections - 1):
            
            for jj in range(100):
                next_waypoint = self._get_next_waypoint(curr_waypoint, distance = 4)
                curr_waypoint = next_waypoint
            world_pose_list.append(curr_waypoint)
            
        return world_pose_list
    
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
    
def main():
    try:
        
        # create the CARLA_ENV helper 
        client = carla.Client("localhost",2000)
        client.set_timeout(10.0)
        world = client.load_world('Town04') # use Town 04 which contains a freeway
        
        # default the weather to be a fine day
        weather = carla.WeatherParameters(
            cloudiness=10.0,
            precipitation=0.0,
            sun_altitude_angle=90.0)
        world.set_weather(weather)
        
        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location(x=-170, y=-151, z=116.5), carla.Rotation(pitch=-33, yaw= 56.9, roll=0.0)))
        
        # create the environment
        env = CARLA_ENV(world)
        time.sleep(2) # sleep for 2 seconds, wait the initialization to finish
        
        freewayenv = FreewayEnv(env,3)
        section_list = freewayenv.get_section_list()
        section_list[0].add_ego_vehicle()
        
        section_list[0].add_full_path_vehicle(vehicle_type = "lead", gap = 10.0 ,choice = "left", command = "lane", command_start_time = 2.0)
        
        section_list[0].add_full_path_vehicle(vehicle_type = "lead",choice = "left", command = "lane", command_start_time = 2.0, vehicle_color = '255,255,255')
        section_list[0].add_full_path_vehicle(vehicle_type = "follow",choice = "subject", command = "lane", command_start_time = 2.0)
        section_list[0].add_full_path_vehicle(vehicle_type = "follow",choice = "subject", vehicle_color = '255,255,255', command = "lane", command_start_time = 2.0)
        section_list[0].add_full_path_vehicle(vehicle_type = "follow",choice = "left", command = "lane", command_start_time = 2.0)
        section_list[0].add_full_path_vehicle(vehicle_type = "follow",choice = "left", vehicle_color = '255,255,255', command = "lane", command_start_time = 2.0)
        section_list[0].add_full_path_vehicle()
        section_list[0].add_full_path_vehicle(vehicle_color = '255,255,255', command = "lane", command_start_time = 2.0)
        
        freewayenv.SectionBackend()
    finally:
        time.sleep(10)
        env.destroy_actors()
        
    
if __name__ == '__main__':
    main()