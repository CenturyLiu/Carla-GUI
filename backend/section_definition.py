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
        
    def get_section_trajectory_points(self):
        # get the reference points of this section for use outside
        return self.reference_way_points
        
    def load_vehicle_settings(self, ego, subject_lead, subject_follow, left_lead, left_follow):
        '''
        load in the vehicle settings from initial intersection

        Parameters
        ----------
        ego : ConfigObj
            DESCRIPTION.
        subject_lead : TYPE
            DESCRIPTION.
        subject_follow : TYPE
            DESCRIPTION.
        left_lead : TYPE
            DESCRIPTION.
        left_follow : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        pass