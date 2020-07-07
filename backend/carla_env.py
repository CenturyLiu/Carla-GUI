#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 13:45:54 2020

@author: shijiliu
"""
import glob
import os
import sys
import time
import random

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass



import carla
import matplotlib.pyplot as plt
import numpy as np
from collections import deque


# color for debug use
red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)

def config_world(world, synchrony = True, delta_seconds = 0.02):
        '''
        Effects
        -------
        Config the carla world's synchrony and time-step
        tutorial: https://carla.readthedocs.io/en/latest/adv_synchrony_timestep/
        
        Parameters
        ----------
        synchrony : TYPE, optional
            DESCRIPTION. The default is True.
        delta_seconds : TYPE, optional
            DESCRIPTION. The default is 0.02.

        Returns
        -------
        synchrony, delta_seconds
        '''
        
        
        settings = world.get_settings()
        settings.synchronous_mode = synchrony
        settings.fixed_delta_seconds = delta_seconds
        world.apply_settings(settings)
        return synchrony, delta_seconds
        
class CARLA_ENV():
    def __init__(self, world):
        
        #self.client = carla.Client('localhost', 2000)
        #self.client.set_timeout(10.0)
        #self.client = client
        #self.world = self.client.get_world()
        self.world = world
        self.blueprint_library = self.world.get_blueprint_library()
        #self.blueprint_library = blueprint_library
        
        self.vehicle_dict = {}
        self.walker_dict = {}
        self.sensor_dict = {}
        self.config_env()
        #self.synchrony = synchrony
        #self.delta_seconds = delta_seconds
        
    def config_env(self, synchrony = False, delta_seconds = 0.02):

        
        self.synchrony = synchrony
        self.delta_seconds = delta_seconds
        settings = self.world.get_settings()
        settings.synchronous_mode = synchrony
        settings.fixed_delta_seconds = delta_seconds
        self.world.apply_settings(settings)
        
    def spawn_vehicle(self, model_name = None, spawn_point = None):
        '''
        Parameters
        ----------
        model_name : str TYPE, optional
            DESCRIPTION:  The default is None.
        spawn_point : carla.Transform() TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        Uniquename of the actor.

        '''
        if model_name == None:
            bp = random.choice(self.blueprint_library.filter('vehicle.*.*'))
        else:
            bp = random.choice(self.blueprint_library.filter(model_name))
        
        if spawn_point == None:
            spawn_point = random.choice(self.world.get_map().get_spawn_points())
        
        vehicle = self.world.spawn_actor(bp,spawn_point)
        self.vehicle_dict[vehicle.type_id + '_' + str(vehicle.id)] = vehicle
        return vehicle.type_id + '_' + str(vehicle.id)
    
    def destroy_vehicle(self, uniquename):
        if uniquename in self.vehicle_dict:
            self.vehicle_dict[uniquename].destroy() # destroy the vehicle in carla
            self.vehicle_dict.pop(uniquename) # remove the vehicle from dictionary
    
    def get_vehicle_bounding_box(self, uniquename):
        '''
        

        Parameters
        ----------
        uniquename : string
            uniquename of a vehicle.

        Returns
        -------
        the carla actor corresponding to the uniquename.
        None type will be sent is uniquename doesn't exist
        

        '''
        ret_vehicle_bb = None
        if uniquename in self.vehicle_dict:
            ret_vehicle_bb = self.vehicle_dict[uniquename].bounding_box.extent
            
            
        return ret_vehicle_bb
        
        
    def destroy_actors(self):
        '''
        Effects
        -------
        Destroy all actors that have been spawned

        Returns
        -------
        None.

        '''
        for index in self.vehicle_dict.keys():
            self.vehicle_dict[index].destroy()
        for index in self.walker_dict.keys():
            self.walker_dict[index].destroy()
        for index in self.sensor_dict.keys():
            self.sensor_dict[index].destroy()
            
        self.vehicle_dict.clear()
        self.walker_dict.clear()
        self.sensor_dict.clear()
        print("destroyed all actors")
        
    def apply_vehicle_control(self, uniquename, vehicle_control):
        '''
        Effects: apply control to a specific vehicle

        Parameters
        ----------
        uniquename : str TYPE
            DESCRIPTION.
        vehicle_control : vehicle control TYPE, https://carla.readthedocs.io/en/latest/python_api/#carla.Vehicle
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        vehicle = self.vehicle_dict[uniquename]
        vehicle.apply_control(vehicle_control)
        
    def get_forward_speed(self, uniquename):
        '''
        Get the forward speed of the vehicle

        Parameters
        ----------
        uniquename : TYPE
            name of the vehicle.

        Returns
        -------
        forward speed of the vehicle.

        '''
        vehicle = self.vehicle_dict[uniquename]
        velocity = vehicle.get_velocity()
        return (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2)**0.5
    
    def get_transform_2d(self, uniquename):
        '''
        

        Parameters
        ----------
        uniquename : str
            name of the vehicle.

        Returns
        -------
        location and orientation of the vehicle.

        '''
        vehicle = self.vehicle_dict[uniquename]
        transform = vehicle.get_transform()
        location_2d = [transform.location.x, transform.location.y]
        yaw = transform.rotation.yaw
        
        return (location_2d,yaw)
    
    def get_traffic_light_state(self, uniquename):
        '''
        

        Parameters
        ----------
        uniquename : str
            name of the vehicle..

        Returns
        -------
        The traffic light state corresponding to this vehicle.
        If no traffic light available, return None

        '''
        vehicle = self.vehicle_dict[uniquename]
        state = None
        if vehicle.is_at_traffic_light():
            light = vehicle.get_traffic_light()
            state = light.get_state()
            
        return state
        
    def draw_waypoints(self, trajectory, points):
        '''
        Draw the way points and trajectory for the vehicle to follow

        Parameters
        ----------
        trajectory : numpy 2d array
            the interpolated trajectory of a vehicle.
        points : list of (x,y)
            waypoints to highlight

        Returns
        -------
        None.

        '''
        for ii in range(len(points) - 1):
            location = carla.Location(x = points[ii][0], y = points[ii][1], z = 5.0)
            self.world.debug.draw_point(location, size = 0.1, color = orange, life_time=0.0, persistent_lines=True)
        
        location = carla.Location(x = points[-1][0], y = points[-1][1], z = 5.0)
        self.world.debug.draw_point(location, size = 0.1, color = red, life_time=0.0, persistent_lines=True)
        
        for ii in range(1,len(trajectory)):
            begin = carla.Location(x = trajectory[ii - 1][0], y = trajectory[ii - 1][1], z = 5.0)
            end = carla.Location(x = trajectory[ii][0], y = trajectory[ii][1], z = 5.0)
            self.world.debug.draw_line(begin, end, thickness=0.8, color=orange, life_time=0.0, persistent_lines=True)
    
    def draw_real_trajectory(self, real_trajectory):
        '''
        Draw the real trajectory

        Parameters
        ----------
        real_trajectory : a deque of 2 (x,y) tuple
            stores the current and previous 2d location of the vehicle

        Returns
        -------
        None.

        '''
        begin = carla.Location(x = real_trajectory[0][0], y = real_trajectory[0][1], z = 5.0)
        end = carla.Location(x = real_trajectory[1][0], y = real_trajectory[1][1], z = 5.0)
        #self.world.debug.draw_arrow(begin, end, thickness=1.0, arrow_size=1.0, color = green, life_time=0.0, persistent_lines=True)
        
'''
client = carla.Client("localhost",2000)
client.set_timeout(2.0)
world = client.load_world('Town03')#'Town06' for plain ground
weather = carla.WeatherParameters(
    cloudiness=10.0,
    precipitation=0.0,
    sun_altitude_angle=90.0)
world.set_weather(weather)
'''
'''
settings = world.get_settings()
#settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.02
world.apply_settings(settings)

settings = world.get_settings()
settings.synchronous_mode = True
world.apply_settings(settings)

#synchrony, delta_seconds = config_world(world)
blueprint_library = world.get_blueprint_library()
'''
'''
env = CARLA_ENV(world)

try:
    name = env.spawn_vehicle()
    print(name)
finally:
    env.destroy_actors()
'''