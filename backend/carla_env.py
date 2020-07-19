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
from configobj import ConfigObj
import math

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
        self.config_env(synchrony = False)
        #self.synchrony = synchrony
        #self.delta_seconds = delta_seconds
        
        self.distance_between_vehicles = ConfigObj() # store the distance between vehicles
        
        
    def config_env(self, synchrony = False, delta_seconds = 0.02):

        
        self.synchrony = synchrony
        self.delta_seconds = delta_seconds
        settings = self.world.get_settings()
        settings.synchronous_mode = synchrony
        settings.fixed_delta_seconds = delta_seconds
        self.world.apply_settings(settings)
        
    def spawn_vehicle(self, model_name = None, spawn_point = None, color = None):
        '''
        Parameters
        ----------
        model_name : str TYPE, optional
            DESCRIPTION:  The default is None.
        spawn_point : carla.Transform() TYPE, optional
            DESCRIPTION. The default is None.
        color : str, optional
            the color of the vehicle

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
        
        if color != None:
            bp.set_attribute('color',color)
        
        
        vehicle = self.world.spawn_actor(bp,spawn_point)
        self.vehicle_dict[vehicle.type_id + '_' + str(vehicle.id)] = vehicle
        return vehicle.type_id + '_' + str(vehicle.id)
    
    def move_vehicle_location(self, uniquename, spawn_point):
        '''
        

        Parameters
        ----------
        uniquename : string
            uniquename of a vehicle.
        spawn_point :  carla.Transform()
            new spawn point of the vehicle

        Returns
        -------
        None.

        '''
        
        
        vehicle = self.vehicle_dict[uniquename]
        vehicle.set_transform(spawn_point)
    
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
        
    def set_vehicle_velocity(self, uniquename, vehicle_velocity):
        '''
        

        Parameters
        ----------
        uniquename : string
            uniquename of vehicle.
        vehicle_velocity : varla.Vector3D
            vehicle speed

        Returns
        -------
        None.

        '''
        vehicle = self.vehicle_dict[uniquename]
        vehicle.set_velocity(vehicle_velocity)
        
        
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
    
    def vehicle_available(self, uniquename):
        '''
        check whether the vehicle exists

        Parameters
        ----------
        uniquename : str
            name of the vehicle.

        Returns
        -------
        exists : bool
            whether the vehicle exists

        '''
        if uniquename in self.vehicle_dict:
            return True
        else:
            return False
    
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
    
    def get_transform_3d(self, uniquename):
        '''
        

        Parameters
        ----------
        uniquename : str
            name of the vehicle.

        Returns
        -------
        3d transform of the vehicle

        '''
        vehicle = self.vehicle_dict[uniquename]
        transform = vehicle.get_transform()
        
        
        return transform
    
    def update_vehicle_distance(self):
        '''
        Update the distance between each 2 vehicles
        This function should be called each world.tick()

        Returns
        -------
        None.

        '''
        self.distance_between_vehicles.reset() # reset the configuration file each update
        
        # get all available vehicles
        vehicle_uniquenames = []
        for name in self.vehicle_dict:
            vehicle_uniquenames.append(name)
            self.distance_between_vehicles[name] = {} # create empty storage
            
        for ii in range(len(vehicle_uniquenames)):
            for jj in range(ii,len(vehicle_uniquenames)):
                name_1 = vehicle_uniquenames[ii]
                name_2 = vehicle_uniquenames[jj]
                if name_1 == name_2:
                    self.distance_between_vehicles[name_1][name_2] = 0.0 # distance with itself, 0.0
                else:
                    vehicle_1 = self.vehicle_dict[name_1]
                    vehicle_2 = self.vehicle_dict[name_2]
                    location_1 = vehicle_1.get_transform().location
                    location_2 = vehicle_2.get_transform().location
                    distance = math.sqrt((location_1.x - location_2.x)**2 + (location_1.y - location_2.y)**2)
                    self.distance_between_vehicles[name_1][name_2] = distance
                    self.distance_between_vehicles[name_2][name_1] = distance
                    
    def check_vehicle_in_front(self, uniquename, safety_distance):
        '''
        

        Parameters
        ----------
        uniquename : str
            name of the vehicle.
            
        safety_distance: float
            allowed closest distance between two vehicles

        Returns
        -------
        has_vehicle_in_front : bool
            whether there exists a vehicle within safety distance
        distance: float
            distance between this vehicle and the vehicle in the front

        '''
        # get the distance between this vehicle and other vehicles
        distance_with_other_vehicle = self.distance_between_vehicles[uniquename]
        
        # get the bounding box of this vehicle
        vehicle_bb = self.vehicle_dict[uniquename].bounding_box.extent
        safety_distance += vehicle_bb.x / 2 # add the half length of the vehicle
        
        has_vehicle_in_front = False
        distance = None
        
        vehicle_1 = self.vehicle_dict[uniquename]
        location_1 = vehicle_1.get_transform().location
        forward_vector = vehicle_1.get_transform().get_forward_vector()
        
        for name in distance_with_other_vehicle:
            if name != uniquename and distance_with_other_vehicle[name] < safety_distance and name in self.vehicle_dict: # a possible vehicle
                location_2 = self.vehicle_dict[name].get_transform().location
                vec1_2 = np.array([location_2.x - location_1.x, location_2.y - location_1.y])
                forward_vector_2d = np.array([forward_vector.x, forward_vector.y])
                
                norm_vec1_2 = vec1_2 / np.linalg.norm(vec1_2)
                norm_forward_vector_2d = forward_vector_2d / np.linalg.norm(forward_vector_2d)
                dot_product = np.dot(norm_vec1_2,norm_forward_vector_2d)
                angle = np.arccos(dot_product)
                
                
                
                if angle < np.arctan(vehicle_bb.y /  vehicle_bb.x):#np.arcsin((vehicle_bb.y  + 1) / distance_with_other_vehicle[name]):#np.arctan(vehicle_bb.y / vehicle_bb.x): 
                    has_vehicle_in_front = True
                    distance = np.dot(vec1_2,forward_vector_2d)
                    break
            
        return has_vehicle_in_front, distance
        
        

    
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