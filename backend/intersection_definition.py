#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 10:20:35 2020

@author: shijiliu
"""


import carla
from carla_env import CARLA_ENV 
import math
import time
import numpy as np
from configobj import ConfigObj
from generate_path_omit_regulation import generate_path
from scipy.interpolate import UnivariateSpline
import copy

DEBUG_INIT = True
DEBUG_TRAJECTORY = True

# color for debug use
red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)


# distance of lane points from traffic light
'''
END1 = -6.5#-5.5
END2 = -9.0
START1 = -12.5
START2 = -15.5#-15.5#-16.0
'''

# right shift from the center of the lane when spawning
RIGHT_SHIFT = 1.6 # 0.0 if requirements changed to spawn in the middle of the lane#

def get_traffic_lights(actor_list):
    # get all the available traffic lights
    traffic_light_list = []
    for actor in actor_list:
        if 'traffic_light' in actor.type_id:
            traffic_light_list.append(actor)
    return traffic_light_list

def smooth_trajectory(trajectory):
    '''
    

    Parameters
    ----------
    trajectory : np.array([(float,float),...,(float,float)])
        2d trajectory.

    Returns
    -------
    smoothed_trajectory : np.array([(float,float),...,(float,float)])
        the smoother trajectory

    '''
    
    smoothed_trajectory = []
    smoothed_trajectory.append(trajectory[0])
    
    num = 3
    
    for ii in range(num - 1,len(trajectory)):
        avg_pt = (trajectory[ii - 2] + trajectory[ii - 1] + trajectory[ii]) / num
        smoothed_trajectory.append(avg_pt)
    
    smoothed_trajectory.append(trajectory[-1])
    return np.array(smoothed_trajectory)

def get_trajectory(way_points):
    '''
    

    Parameters
    ----------
    way_points : list
        A list of (way_point, reference_speed) tuple, 
        where way_points is a tuple of floats (x,y), the first point must be the **current point** of the vehicle
              reference speed is the desired speed for the vehicle after this way point and before the next way point
        e.g. [((0.0,0.0),10.0),((0.0,10.0),1.0)]

    Returns
    -------
    trajectory : numpy 2d array
        the interpolated trajectory.
    ref_speed_list : list
        the speed correspoding to the interpolated trajectory

    '''
    points, speed = zip(*way_points)
    points = np.array([[pt[0], pt[1]] for pt in points])
    
    # apply average smoothing of the points
    points = smooth_trajectory(points)
    
    # linear length along the line (reference: https://stackoverflow.com/questions/52014197/how-to-interpolate-a-2d-curve-in-python)
    distance = np.cumsum( np.sqrt(np.sum( np.diff(points,axis=0)**2, axis = 1)))
    distance = np.insert(distance, 0, 0)/distance[-1]
    
    '''
    # define interpolation method
    interpolation_method = 'slinear' #'quadratic'
    
    alpha = np.linspace(0,1, 2 * len(distance))
    
    interpolator = interp1d(distance, points, kind = interpolation_method, axis = 0)
    trajectory = interpolator(alpha)
    '''
    
    # Build a list of the spline function, one for each dimension:
    splines = [UnivariateSpline(distance, coords, k=3, s=.2) for coords in points.T]
    
    alpha = np.linspace(0,1.0, 2 * len(distance))
    trajectory = np.vstack( [spl(alpha) for spl in splines] ).T
    
    
    nearest_index = []
    for pt in points:
        nearest_distance = np.inf
        index = 0
        count = 0
        for trajectory_pt in trajectory:
            dist_2 = sum((trajectory_pt - pt)**2)
            if dist_2 < nearest_distance:
                nearest_distance = dist_2
                index = count
            count += 1
        nearest_index.append(index)
        
    ref_speed_list = np.zeros(len(trajectory))
    for ii in range(1,len(nearest_index)):
        ref_speed_list[nearest_index[ii - 1]:nearest_index[ii]] = speed[ii - 1]
    
    #plt.plot(trajectory[:,0],trajectory[:,1],'.')
    #print(ref_speed_list)
    
    return trajectory, ref_speed_list

class Intersection():
    def __init__(self, env, world_pos, traffic_light_list, distance = 75.0, yaw = 0.0, start_sim_distance = 40):
        '''
        

        Parameters
        ----------
        env: CARLA_ENV
            the simulation environment
        world_pos : (float,float)
            the (rough) central point of the intersection.
        traffic_light_list : list
            list of all available traffic lights.
        distance : float, optional
            width and height of the intersection. The default is 75.0 (m).
        yaw : float, optional
            define the direction the ego vehicle will pass through the intersection. The default is 0.

        Returns
        -------
        None.

        '''
        
        self.env = env
        self.distance = distance
        self.yaw = yaw % 360
        self._get_local_traffic_lights(world_pos,traffic_light_list) # get the traffic light at this intersection
        self._get_lane_points() # get the in/out point of lane
        #self._yaw2vector()
        self._split_lane_points() # split in/out point of lane into subject/left/right/ahead
        self._get_spawn_reference() # find a reference point for spawning for each of the subject/left/right/ahead lane
        self._split_traffic_lights() # split the traffic lights into subject/left/right/ahead
        
        self.subject_vehicle = []
        self.left_vehicle = []
        self.right_vehicle = []
        self.ahead_vehicle = []
        
        self.start_sim_distance = start_sim_distance
        self.start_sim = False # whether the simulation at this intersection should start or not
        
        self.DEBUG_TRAJECTORY = True
        
    def start_simulation(self, full_path_vehicle_name):
        '''
        check whether the first full path vehicle is within this intersection

        Parameters
        ----------
        full_path_vehicle_name : string
            uniquename of the first full path vehicle (i.e. lead if lead exists, otherwise ego)

        Returns
        -------
        None.

        '''
        full_path_vehicle_transform = self.env.get_transform_2d(full_path_vehicle_name)
        full_path_vehicle_location = full_path_vehicle_transform[0] # 2d location of the vehicle
        ref_waypoint = self.subject_lane_ref
        ref_location = ref_waypoint.transform.location
        distance = math.sqrt((ref_location.x - full_path_vehicle_location[0])**2 + (ref_location.y - full_path_vehicle_location[1])**2 )
       
        # start simulation if distance between the vehicle and the reference point is within 
        # the pre-set start_sim_distance
        if distance < self.start_sim_distance:
            self.start_sim = True
        
        
        
    def _get_local_traffic_lights(self, world_pos,traffic_light_list):
        '''
        

        Parameters
        ----------
        world_pos : (float,float)
            the (rough) central point of the intersection.
        traffic_light_list : list
            list of all available traffic lights.

        Returns
        -------
        None.

        '''
        self.local_traffic_lights = []
        for light in traffic_light_list:
            location = light.get_location()
            distance = math.sqrt((location.x - world_pos[0])**2 + (location.y - world_pos[1]) ** 2) # get the 2d Euclidean distance
            if distance < self.distance / 2:
                self.local_traffic_lights.append(light)
                
        assert(len(self.local_traffic_lights) == 4) # should contain and only contain 4 lights
        
        x = 0
        y = 0
        for light in self.local_traffic_lights:
            x += light.get_location().x
            y += light.get_location().y
        
        self.world_pos = (x / len(self.local_traffic_lights),y / len(self.local_traffic_lights)) 
        
        
        if DEBUG_INIT:
            print(self.world_pos)
            for light in self.local_traffic_lights:
                print(light.get_location())
                self.env.world.debug.draw_point(light.get_location(),size = 0.1, color = blue, life_time=0.0, persistent_lines=True)
                

    def _get_lane_points(self):
        # get the into/out lane points of this intersection
        self.carla_map = self.env.world.get_map()
        self.out_lane_points = []
        self.into_lane_points = []
        
        '''
        for light in self.local_traffic_lights:
            light_location = light.get_location()
            vector = light.get_transform().get_forward_vector()
            end_1 = carla.Location(x = light_location.x + vector.x * END1,y = light_location.y + vector.y * END1, z = light_location.z + vector.z * END1) 
            end_2 = carla.Location(x = light_location.x + vector.x * END2,y = light_location.y + vector.y * END2, z = light_location.z + vector.z * END2)
            start_1 = carla.Location(x = light_location.x + vector.x * START1,y = light_location.y + vector.y * START1, z = light_location.z + vector.z * START1)
            start_2 = carla.Location(x = light_location.x + vector.x * START2,y = light_location.y + vector.y * START2, z = light_location.z + vector.z * START2)
            into_1 = self.carla_map.get_waypoint(end_1)
            into_2 = self.carla_map.get_waypoint(end_2)
            out_1 = self.carla_map.get_waypoint(start_1)
            out_2 = self.carla_map.get_waypoint(start_2)
            self.out_lane_points.append(out_1)
            self.out_lane_points.append(out_2)
            self.into_lane_points.append(into_1)
            self.into_lane_points.append(into_2)
        '''
        for ii in range(len(self.local_traffic_lights)):
            light_location = self.local_traffic_lights[ii].get_location()
            vector = self.local_traffic_lights[ii].get_transform().get_forward_vector()
            for jj in range(len(self.local_traffic_lights)):
                if jj != ii:
                    # calculate the angle between the light's forward vector and 
                    # the vector from this light to the other light
                    another_light_location = self.local_traffic_lights[jj].get_location()
                    vec1_2 = np.array([another_light_location.x - light_location.x, another_light_location.y - light_location.y])
                    forward_vector_2d = np.array([-vector.x, -vector.y]) # the reverse direction of forward vector is what we need
                    norm_vec1_2 = vec1_2 / np.linalg.norm(vec1_2)
                    norm_forward_vector_2d = forward_vector_2d / np.linalg.norm(forward_vector_2d)
                    dot_product = np.dot(norm_vec1_2,norm_forward_vector_2d)
                    angle = np.arccos(dot_product)
                    
                    
                    if angle < np.pi / 12: # angle within 15 degrees
                        other_light_location = another_light_location
                        break
                    
                    
            distance = math.sqrt((light_location.x - other_light_location.x)**2 + (light_location.y - other_light_location.y)**2)
            
            
            if distance < 25: # 4 lanes inside
                END1 = -6.5#-5.5
                END2 = -9.0
                START1 = -12.5
                START2 = -15.5#-15.5#-16.0
            elif distance >= 25 and distance < 27:
                # 6 lane road
                END1 = -8.0#-5.5
                END2 = -12.0
                START1 = -16.0
                START2 = -18.0#-15.5#-16.0
            else:
                # 6 lane road, wider
                END1 = -9.0#-5.5
                END2 = -12.0
                START1 = -16.0
                START2 = -20.0#-15.5#-16.0
            
            
            end_1 = carla.Location(x = light_location.x + vector.x * END1,y = light_location.y + vector.y * END1, z = light_location.z + vector.z * END1) 
            end_2 = carla.Location(x = light_location.x + vector.x * END2,y = light_location.y + vector.y * END2, z = light_location.z + vector.z * END2)
            start_1 = carla.Location(x = light_location.x + vector.x * START1,y = light_location.y + vector.y * START1, z = light_location.z + vector.z * START1)
            start_2 = carla.Location(x = light_location.x + vector.x * START2,y = light_location.y + vector.y * START2, z = light_location.z + vector.z * START2)
            into_1 = self.carla_map.get_waypoint(end_1)
            into_2 = self.carla_map.get_waypoint(end_2)
            out_1 = self.carla_map.get_waypoint(start_1)
            out_2 = self.carla_map.get_waypoint(start_2)
            self.out_lane_points.append(out_1)
            self.out_lane_points.append(out_2)
            self.into_lane_points.append(into_1)
            self.into_lane_points.append(into_2)
        
    def _yaw2vector(self):
        # get the direction vector of this intersection
        yaw_rad = math.radians(self.yaw)
        self.direction_vector = [math.cos(yaw_rad),math.sin(yaw_rad)]
        
    def _debug_lane_point(self,pt,color):
        if DEBUG_INIT:
            self.env.world.debug.draw_point(pt.transform.location,size = 0.1, color = color, life_time=0.0, persistent_lines=True)
            forward_vector = pt.transform.get_forward_vector()
            start = pt.transform.location
            end = carla.Location(x = start.x + forward_vector.x, y = start.y + forward_vector.y, z = start.z + forward_vector.z)
            self.env.world.debug.draw_arrow(start,end,thickness=0.1, arrow_size=0.2, color = color, life_time=0.0, persistent_lines=True)
        
    def _split_lane_points(self):
        # split the lane points into 
        # subject/left/right/ahead lane
        
        self.subject_out = []
        self.left_out = []
        self.right_out = []
        self.ahead_out = []
        
        self.subject_in = []
        self.left_in = []
        self.right_in = []
        self.ahead_in = []
        
        max_angle_dev = 10
        
        for pt in self.out_lane_points:
            pt_yaw = pt.transform.rotation.yaw % 360
            relative_yaw = (pt_yaw - self.yaw) % 360
            
            if abs(relative_yaw - 0) < max_angle_dev or abs(relative_yaw - 360) < max_angle_dev:
                self.subject_out.append(pt)
                self._debug_lane_point(pt,green)
                
            elif abs(relative_yaw - 90) < max_angle_dev:
                self.left_out.append(pt)
                self._debug_lane_point(pt,blue)
                
            elif abs(relative_yaw - 180) < max_angle_dev:
                self.ahead_out.append(pt)
                self._debug_lane_point(pt,yellow)
                
            elif abs(relative_yaw - 270) < max_angle_dev:
                self.right_out.append(pt)
                self._debug_lane_point(pt,orange)
        
        for pt in self.into_lane_points:
            pt_yaw = pt.transform.rotation.yaw % 360
            relative_yaw = (pt_yaw - self.yaw) % 360
            if abs(relative_yaw - 0) < max_angle_dev or abs(relative_yaw - 360) < max_angle_dev:
                self.ahead_in.append(pt)
                self._debug_lane_point(pt,green)
                
            elif abs(relative_yaw - 90) < max_angle_dev :
                self.right_in.append(pt)
                self._debug_lane_point(pt,blue)
                
            elif abs(relative_yaw - 180) < max_angle_dev:
                self.subject_in.append(pt)
                self._debug_lane_point(pt,yellow)
                
            elif abs(relative_yaw - 270) < max_angle_dev:
                self.left_in.append(pt)
                self._debug_lane_point(pt,orange)
                
    def _split_traffic_lights(self):
        # split the traffic lights into 
        # subject/left/right/ahead lane
        
        # get the 4 direction vector
        forward_direction = self.subject_lane_ref.transform.get_forward_vector()
        forward_direction_2d = [forward_direction.x,forward_direction.y]
        forward_direction_2d = forward_direction_2d / np.linalg.norm(forward_direction_2d)
        
        left_direction = self.left_lane_ref.transform.get_forward_vector()
        left_direction_2d = [left_direction.x,left_direction.y]
        left_direction_2d = left_direction_2d / np.linalg.norm(left_direction_2d)
        
        right_direction = self.right_lane_ref.transform.get_forward_vector()
        right_direction_2d = [right_direction.x,right_direction.y]
        right_direction_2d = right_direction_2d / np.linalg.norm(right_direction_2d)
        
        ahead_direction = self.ahead_lane_ref.transform.get_forward_vector()
        ahead_direction_2d = [ahead_direction.x,ahead_direction.y]
        ahead_direction_2d = ahead_direction_2d / np.linalg.norm(ahead_direction_2d)
        
        self.subject_light = None
        self.left_light = None
        self.right_light = None
        self.ahead_light = None
        
        for traffic_light in self.local_traffic_lights:
            light_vector = traffic_light.get_transform().get_forward_vector()
            left_vector = self._get_left_vector(light_vector)
            if abs(np.dot(left_vector,forward_direction_2d) - 1.0) < 0.1:
                self.subject_light = traffic_light
            elif abs(np.dot(left_vector,left_direction_2d) - 1.0) < 0.1:
                self.left_light = traffic_light
            elif abs(np.dot(left_vector,right_direction_2d) - 1.0) < 0.1:
                self.right_light = traffic_light
            elif abs(np.dot(left_vector,ahead_direction_2d) - 1.0) < 0.1:
                self.ahead_light = traffic_light
        
        self.light_config = ConfigObj()
        self.light_config["subject"] = None
        self.light_config["subject_time"] = None
        self.light_config["left"] = None
        self.light_config["left_time"] = None
        self.light_config["right"] = None
        self.light_config["right_time"] = None
        self.light_config["ahead"] = None
        self.light_config["ahead_time"] = None
        
        # initialize counter for traffic light color setting
        self.local_time_count = 0
        
        
        if DEBUG_INIT:
            self.env.world.debug.draw_point(self.subject_light.get_transform().location,size = 0.2, color = green, life_time=0.0, persistent_lines=True)
            self.env.world.debug.draw_point(self.left_light.get_transform().location,size = 0.2, color = yellow, life_time=0.0, persistent_lines=True)
            self.env.world.debug.draw_point(self.right_light.get_transform().location,size = 0.2, color = blue, life_time=0.0, persistent_lines=True)
            self.env.world.debug.draw_point(self.ahead_light.get_transform().location,size = 0.2, color = red, life_time=0.0, persistent_lines=True)
            
    def _get_left_vector(self,vector):
        # return the left vector of the input 2d vector
        # vector : carla.Vector3D
        left_x = vector.y
        left_y = - vector.x
        return [left_x,left_y]
        
                
    def _vec_angle(self,vec1,vec2):
        vec1 = vec1 / np.linalg.norm(vec1)
        vec2 = vec2 / np.linalg.norm(vec2)
        dot_product = np.dot(vec1,vec2)
        angle = np.arccos(dot_product)
        return angle
                
        
    def _get_lane_spawn_reference(self,lane_out_pts):
        # function: return the reference point for spawning in this lane
        
        # requirements: lane_out_pts should have and only have 2 points
        # in theory, the second point should be more "left"

        
        return lane_out_pts[1]
    
    def _get_spawn_reference(self):
        # get the reference way point for each lane
        self.subject_lane_ref = self._get_lane_spawn_reference(self.subject_out)
        self.left_lane_ref = self._get_lane_spawn_reference(self.left_out)
        self.right_lane_ref = self._get_lane_spawn_reference(self.right_out)
        self.ahead_lane_ref = self._get_lane_spawn_reference(self.ahead_out)
        
        if DEBUG_INIT:
            self.env.world.debug.draw_point(self.subject_lane_ref.transform.location,size = 0.2, color = green, life_time=0.0, persistent_lines=True)
            self.env.world.debug.draw_point(self.left_lane_ref.transform.location,size = 0.2, color = yellow, life_time=0.0, persistent_lines=True)
            self.env.world.debug.draw_point(self.right_lane_ref.transform.location,size = 0.2, color = blue, life_time=0.0, persistent_lines=True)
            self.env.world.debug.draw_point(self.ahead_lane_ref.transform.location,size = 0.2, color = red, life_time=0.0, persistent_lines=True)
        
    def add_vehicle(self,gap = 10.0,model_name = "vehicle.tesla.model3",choice = "subject", command = "straight", stop_choice = "normal", penetrate_distance = None,obey_traffic_lights = True, run = True, safety_distance = 15.0):    
        '''
        

        Parameters
        ----------
        gap : float,optional
            the distance between a vehicle and its previous one
        model_name : string, optional
            vehicle type. The default is "vehicle.tesla.model3".
        choice : string, optional
            the lane this vehicle will be added, valid values: "subject", "left", "right", "ahead". The default is "subject".
        command : string, optional
            the turning command, valid values: "straight", "right", "left"
        stop_choice : string, optional
            how will the vehicle stop when at yellow or red light. valid values: "normal", "abrupt", "penetrate"
        penetrate_distance : float, unit: meter
            to what extent the vehicle will penetrate the traffic lane. This parameter will only be use when stop_choice is "penetrate"
        obey_traffic_light : bool, optional
            whether the vehicle will obey traffic light. Default is True
        run : bool, optional
            whether the vehicle is running. Default is True
        safety_distance : float, optional
            smallest distance between this vehicle and vehicle ahead

        Returns
        -------
        uniquename : the uniquename of the vehicle

        '''
        
        right_shift_value = RIGHT_SHIFT
        
        vehicle = ConfigObj()
        vehicle["model"] = model_name
        vehicle["gap"] = gap
        vehicle["command"] = command
        vehicle["obey_traffic_lights"] = obey_traffic_lights
        vehicle["run"] = run
        vehicle["safety_distance"] = safety_distance
        vehicle["choice"] = choice
        
        if choice == "subject":
            ref_waypoint = self.subject_lane_ref
            vehicle_set = self.subject_vehicle
        elif choice == "left":
            ref_waypoint = self.left_lane_ref
            vehicle_set = self.left_vehicle
        elif choice == "ahead":
            ref_waypoint = self.ahead_lane_ref
            vehicle_set = self.ahead_vehicle
        elif choice == "right":
            ref_waypoint = self.right_lane_ref
            vehicle_set = self.right_vehicle
        
        if len(vehicle_set) != 0:
            ref_waypoint = vehicle_set[-1]["ref_waypoint"]
            #previous_uniquename = vehicle_set[-1]["uniquename"]
            #bb = self.env.get_vehicle_bounding_box(previous_uniquename)
            bb = vehicle_set[-1]["bounding_box"]
            
            right_shift_value = right_shift_value #- bb.y / 2
            gap += bb.x
        
        else:
            if gap < 10.0:
                gap = 10.0 # add a constraint to the gap between the first vehicle and the lane 
                           # reference point. Add a vehicle too close to reference point
                           # will lead to vehicle not detecting the traffic light
                           
        
        # use the original reference point to get the new reference point
        # reference point is in the middle of the lane
        # function same as self._get_next_waypoint
        forward_vector = ref_waypoint.transform.get_forward_vector()

        location = ref_waypoint.transform.location
        raw_spawn_point = carla.Location(x = location.x - gap * forward_vector.x  , y = location.y - gap * forward_vector.y , z = location.z + 1.0)
        
        new_ref_waypoint = self.carla_map.get_waypoint(raw_spawn_point)
        
        # right shift the spawn point
        # right is with respect to the direction of vehicle navigation
        ref_yaw = new_ref_waypoint.transform.rotation.yaw
        
        right_vector = self._get_unit_right_vector(ref_yaw)
        
        new_location = new_ref_waypoint.transform.location
        
        spawn_location = carla.Location(x = new_location.x - right_shift_value * right_vector[0], y = new_location.y -  right_shift_value * right_vector[1], z = new_location.z + 0.1)
        spawn_rotation = new_ref_waypoint.transform.rotation
        
        uniquename = self.env.spawn_vehicle(model_name = model_name,spawn_point = carla.Transform(spawn_location,spawn_rotation)) 
        vehicle["uniquename"] = uniquename
        vehicle["ref_waypoint"] = new_ref_waypoint
        vehicle["location"] = spawn_location
        vehicle["rotation"] = spawn_rotation
        
        
        
        trajectory, ref_speed_list = self._generate_path(choice, command, new_ref_waypoint)
        vehicle["trajectory"] = trajectory
        vehicle["ref_speed_list"] = ref_speed_list
        
        # get the bounding box of the new vehicle
        
        new_bb = self.env.get_vehicle_bounding_box(uniquename)
        vehicle["bounding_box"] = new_bb
        vehicle["vehicle_type"] = "other"
        
        # vehicle stop type
        vehicle["stop_choice"] = stop_choice
        vehicle["penetrate_distance"] = penetrate_distance
        if stop_choice == "normal":
            stop_point = self._get_next_waypoint(ref_waypoint,distance = -3.0) # 3 meters after the reference point
            vehicle["stop_ref_point"] = stop_point.transform.location
        elif stop_choice == "penetrate":
            stop_point = self._get_next_waypoint(ref_waypoint,distance = penetrate_distance)
            vehicle["stop_ref_point"] = stop_point.transform.location
        else:
            vehicle["stop_ref_point"] = None
        
        
        
        
        vehicle_set.append(vehicle)
        
        return uniquename
    
    def _shift_vehicles(self, length, choice = "subject", index = 0):
        '''
        shift the location of a list of vehicles
        
        **note: for ego/lead/follow type, the path is not generated**

        Parameters
        ----------
        length : float
            the length we want to shift all the vehicles
        choice : string, optional
            the lane this vehicle will be added, valid values: "subject", "left", "right", "ahead". The default is "subject". 
        index : int, optional
            the index of the vehicle that shifting. The default is 0.

        Returns
        -------
        None.

        '''
        right_shift_value = RIGHT_SHIFT
        
        if choice == "subject":
            #ref_waypoint = self.subject_lane_ref
            vehicle_set = self.subject_vehicle
        elif choice == "left":
            #ref_waypoint = self.left_lane_ref
            vehicle_set = self.left_vehicle
        elif choice == "ahead":
            #ref_waypoint = self.ahead_lane_ref
            vehicle_set = self.ahead_vehicle
        elif choice == "right":
            #ref_waypoint = self.right_lane_ref
            vehicle_set = self.right_vehicle
            
        #if index != 0:
        #    ref_waypoint = vehicle_set[index - 1]["ref_waypoint"]
            
        # shifting the vehicles in reverse order
        for ii in range(len(vehicle_set) - 1,index - 1,-1):
            vehicle = vehicle_set[ii]
            new_ref_waypoint = self._get_next_waypoint(vehicle["ref_waypoint"],distance = length)
        
            ref_yaw = new_ref_waypoint.transform.rotation.yaw
        
            right_vector = self._get_unit_right_vector(ref_yaw)
        
            new_location = new_ref_waypoint.transform.location
        
            spawn_location = carla.Location(x = new_location.x - right_shift_value * right_vector[0], y = new_location.y -  right_shift_value * right_vector[1], z = new_location.z + 0.1)
            spawn_rotation = new_ref_waypoint.transform.rotation
            
            # move the vehicle location
            self.env.move_vehicle_location(vehicle["uniquename"],carla.Transform(spawn_location,spawn_rotation))
            vehicle["ref_waypoint"] = new_ref_waypoint
            vehicle["location"] = spawn_location
            vehicle["rotation"] = spawn_rotation
            
            if vehicle["vehicle_type"] == "other":
                command = vehicle["command"]
                trajectory, ref_speed_list = self._generate_path(choice, command, new_ref_waypoint) # generate new trajectory
                vehicle["trajectory"] = trajectory
                vehicle["ref_speed_list"] = ref_speed_list
                
            
        
        
        
    
    def _get_unit_right_vector(self,yaw):
        # get the right vector
        right_yaw = (yaw + 270) % 360
        rad_yaw = math.radians(right_yaw)
        right_vector = [math.cos(rad_yaw),math.sin(rad_yaw)]
        right_vector = right_vector / np.linalg.norm(right_vector)
        return right_vector
        
    
    def _generate_path(self, choice, command, start_waypoint):
        '''
        

        Parameters
        ----------
        choice : string
            the lane choice, valid values: "subject","left","right","ahead"
        command : string
            the command of navigation. valid command: "straight","left","right"

        Returns
        -------
        smoothed_full_trajectory : list of 2d points
             smoothed and interpolated trajectory

        ref_speed_list : list
             the speed correspoding to the interpolated trajectory
        '''
        color = green
        
        if choice == "subject":
            first_waypoint = self.subject_lane_ref
            straight_waypoint = self.ahead_in[0] # can also be [1], choosing the left lane
            left_waypoint = self.left_in[0]
            right_waypoint = self.right_in[0]
            
            
        elif choice == "left":
            first_waypoint = self.left_lane_ref
            straight_waypoint = self.right_in[0] # can also be [1], choosing the left lane
            left_waypoint = self.ahead_in[0]
            right_waypoint = self.subject_in[0]
            
        elif choice == "ahead":
            first_waypoint = self.ahead_lane_ref
            straight_waypoint = self.subject_in[0] # can also be [1], choosing the left lane
            left_waypoint = self.right_in[0]
            right_waypoint = self.left_in[0]
            
        elif choice == "right":
            first_waypoint = self.right_lane_ref
            straight_waypoint = self.left_in[0] # can also be [1], choosing the left lane
            left_waypoint = self.subject_in[0]
            right_waypoint = self.ahead_in[0]
            
        #self.env.world.debug.draw_point(start_waypoint.transform.location,size = 0.5, color = red, life_time=0.0, persistent_lines=True)
            
        if command == "straight":
            second_waypoint = straight_waypoint
        elif command == "left":
            #first_waypoint = self._get_next_waypoint(first_waypoint,3)
            second_waypoint = left_waypoint
            color = yellow
        elif command == "right":
            second_waypoint = right_waypoint
            color = blue
            
        third_waypoint = self._get_next_waypoint(second_waypoint,20)
        trajectory1 = generate_path(self.env, start_waypoint, first_waypoint, waypoint_separation = 4)
        trajectory2 = generate_path(self.env, first_waypoint, second_waypoint,waypoint_separation = 4)
        trajectory3 = generate_path(self.env, second_waypoint, third_waypoint)
        full_trajectory = trajectory1 + trajectory2[1:] + trajectory3[1:] # append the full trajectory
        
        trajectory = [((pt[0],pt[1]),10.0) for pt in full_trajectory]
        
        smoothed_full_trajectory, ref_speed_list = get_trajectory(trajectory) 
        
        if self.DEBUG_TRAJECTORY:
            for ii in range(1,len(smoothed_full_trajectory)):
                loc1 = carla.Location(x = smoothed_full_trajectory[ii - 1][0], y = smoothed_full_trajectory[ii - 1][1], z = 0.0)
                loc2 = carla.Location(x = smoothed_full_trajectory[ii][0], y = smoothed_full_trajectory[ii][1], z = 0.0)
                self.env.world.debug.draw_arrow(loc1, loc2, thickness = 0.05, arrow_size = 0.1, color = color, life_time=0.0, persistent_lines=True)
        return smoothed_full_trajectory, ref_speed_list
    
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
        
    def get_subject_waypoints(self):
        first_waypoint = self.subject_lane_ref
        second_waypoint = self.ahead_in[0]
        third_waypoint = self._get_next_waypoint(second_waypoint,20)
        return [first_waypoint,second_waypoint,third_waypoint]


    def remove_vehicle(self,uniquename):
        '''
        remove a specific vehicle from the intersection

        Parameters
        ----------
        uniquename : TYPE
            DESCRIPTION.

        Returns
        -------
        removed : Bool, 
            whether a vehicle is removed

        '''
        for ii in range(len(self.subject_vehicle)):
            if self.subject_vehicle[ii]["uniquename"] == uniquename: # check whether the vehicle is the one we want to remove
                # remove vehicle from environment
                self.env.destroy_vehicle(uniquename)
                self.subject_vehicle.pop(ii)
                return True
            
        for ii in range(len(self.left_vehicle)):
            if self.left_vehicle[ii]["uniquename"] == uniquename: # check whether the vehicle is the one we want to remove
                # remove vehicle from environment
                self.env.destroy_vehicle(uniquename)
                self.left_vehicle.pop(ii)
                return True

        for ii in range(len(self.right_vehicle)):
            if self.right_vehicle[ii]["uniquename"] == uniquename: # check whether the vehicle is the one we want to remove
                # remove vehicle from environment
                self.env.destroy_vehicle(uniquename)
                self.right_vehicle.pop(ii)
                return True
            
        for ii in range(len(self.ahead_vehicle)):
            if self.ahead_vehicle[ii]["uniquename"] == uniquename: # check whether the vehicle is the one we want to remove
                # remove vehicle from environment
                self.env.destroy_vehicle(uniquename)
                self.ahead_vehicle.pop(ii)
                return True

        return False

    def edit_traffic_light(self,light, red_start = 0.0,red_end = 10.0,yellow_start = 10.0,yellow_end = 15.0,green_start = 15.0,green_end = 25.0):
        '''
        edit the start and end time for traffic colors
        the traffic color timeline will not loop
        i.e. after it reaches the end of timeline, the traffic state will be 
        frozen at that state
        
        Requirements: there exists and only exists one start time at 0
                      otherwise, a red color will be used as placeholder
                      until the first start time

        Parameters
        ----------
        light : string
            light choice. valid values: ahead,left,right,subject
        

        Returns
        -------
        None.
        '''
        red_start = red_start / self.env.delta_seconds
        red_end = red_end / self.env.delta_seconds
        yellow_start = yellow_start / self.env.delta_seconds
        yellow_end = yellow_end / self.env.delta_seconds
        green_start = green_start / self.env.delta_seconds
        green_end = green_end / self.env.delta_seconds
        
        
        # get the end of timeline
        max_time = max(red_end,yellow_end,green_end)
        
        color_timeline = []
        
        for ii in range(int(max_time)):
            if ii >= red_start and ii < red_end:
                color_timeline.append('red')
            elif ii >= yellow_start and ii < yellow_end:
                color_timeline.append('yellow')
            elif ii >= green_start and ii < green_end:
                color_timeline.append('green')
            else:
                color_timeline.append('red')
        
        self.light_config[light] = color_timeline
        self.light_config[light + '_time'] = {}
        self.light_config[light + '_time']['red'] = red_end - red_start
        self.light_config[light + '_time']['yellow'] = yellow_end - yellow_start
        self.light_config[light + '_time']['green'] = green_end - green_start
        
    def set_intersection_traffic_lights(self):
        # if any traffic light has been set, use the traffic light setting
        # otherwise, do nothing and exit
        # call this function each time after a world.tick()
        
        if self.light_config["subject"] != None:
            if len(self.light_config["subject"]) > self.local_time_count: 
                setting = self.light_config["subject"][self.local_time_count]
                #print(setting)
                light = self.subject_light
                light_state = light.get_state()
                if setting == 'red':
                    if light_state != carla.TrafficLightState.Red: # only set color when the current state is not what we want
                        light.set_state(carla.TrafficLightState.Red)
                        light.set_red_time(self.light_config['subject_time']['red'])
                        light.freeze(True)
                elif setting == 'yellow':
                    if light_state != carla.TrafficLightState.Yellow:
                        light.set_state(carla.TrafficLightState.Yellow)
                        light.set_yellow_time(self.light_config['subject_time']['yellow'])
                        light.freeze(True)
                else:
                    if light_state != carla.TrafficLightState.Green:
                        light.set_state(carla.TrafficLightState.Green)
                        light.set_yellow_time(self.light_config['subject_time']['green'])
                        light.freeze(True)
        
        if self.light_config["left"] != None:
            if len(self.light_config["left"]) > self.local_time_count: 
                setting = self.light_config["left"][self.local_time_count]
                light = self.left_light
                light_state = light.get_state()
                if setting == 'red':
                    if light_state != carla.TrafficLightState.Red: # only set color when the current state is not what we want
                        light.set_state(carla.TrafficLightState.Red)
                        light.set_red_time(self.light_config['left_time']['red'])
                        light.freeze(True)
                elif setting == 'yellow':
                    if light_state != carla.TrafficLightState.Yellow:
                        light.set_state(carla.TrafficLightState.Yellow)
                        light.set_yellow_time(self.light_config['left_time']['yellow'])
                        light.freeze(True)
                else:
                    if light_state != carla.TrafficLightState.Green:
                        light.set_state(carla.TrafficLightState.Green)
                        light.set_yellow_time(self.light_config['left_time']['green'])
                        light.freeze(True)
                    
        if self.light_config["right"] != None:
            if len(self.light_config["right"]) > self.local_time_count: 
                setting = self.light_config["right"][self.local_time_count]
                light = self.right_light
                light_state = light.get_state()
                if setting == 'red':
                    if light_state != carla.TrafficLightState.Red: # only set color when the current state is not what we want
                        light.set_state(carla.TrafficLightState.Red)
                        light.set_red_time(self.light_config['right_time']['red'])
                        light.freeze(True)
                elif setting == 'yellow':
                    if light_state != carla.TrafficLightState.Yellow:
                        light.set_state(carla.TrafficLightState.Yellow)
                        light.set_yellow_time(self.light_config['right_time']['yellow'])
                        light.freeze(True)
                else:
                    if light_state != carla.TrafficLightState.Green:
                        light.set_state(carla.TrafficLightState.Green)
                        light.set_yellow_time(self.light_config['right_time']['green'])
                        light.freeze(True)
        
        if self.light_config["ahead"] != None:
            if len(self.light_config["ahead"]) > self.local_time_count: 
                setting = self.light_config["ahead"][self.local_time_count]
                light = self.ahead_light
                light_state = light.get_state()
                if setting == 'red':
                    if light_state != carla.TrafficLightState.Red: # only set color when the current state is not what we want
                        light.set_state(carla.TrafficLightState.Red)
                        light.set_red_time(self.light_config['ahead_time']['red'])
                        light.freeze(True)
                elif setting == 'yellow':
                    if light_state != carla.TrafficLightState.Yellow:
                        light.set_state(carla.TrafficLightState.Yellow)
                        light.set_yellow_time(self.light_config['ahead_time']['yellow'])
                        light.freeze(True)
                else:
                    if light_state != carla.TrafficLightState.Green:
                        light.set_state(carla.TrafficLightState.Green)
                        light.set_yellow_time(self.light_config['ahead_time']['green'])
                        light.freeze(True)
        
        # update the time count
        self.local_time_count += 1
        
    def export_settings(self):
        '''
        export all settings for a specific intersection

        Returns
        -------
        intersection_settings : ConfigObj
            settings of the intersection

        '''
        intersection_settings = ConfigObj()
        
        # vehicles
        intersection_settings["subject_vehicle"] = []
        intersection_settings["left_vehicle"] = []
        intersection_settings["right_vehicle"] = []
        intersection_settings["ahead_vehicle"] = []
        
        for vehicle in self.subject_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["subject_vehicle"].append(new_vehicle)
        
        for vehicle in self.left_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["left_vehicle"].append(new_vehicle)
            
        for vehicle in self.right_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["right_vehicle"].append(new_vehicle)
            
        for vehicle in self.ahead_vehicle:
            # deep copy the vehicle settings
            new_vehicle = self._copy_vehicle_settings(vehicle)
            intersection_settings["ahead_vehicle"].append(new_vehicle)
        
        # lights
        intersection_settings["subject_light"] = copy.copy(self.light_config["subject"])
        intersection_settings["subject_light_time"] = copy.copy(self.light_config["subject_time"])
        
        intersection_settings["left_light"] = copy.copy(self.light_config["left"])
        intersection_settings["left_light_time"] = copy.copy(self.light_config["left_time"])
        
        intersection_settings["right_light"] = copy.copy(self.light_config["right"])
        intersection_settings["right_light_time"] = copy.copy(self.light_config["right_time"])
        
        intersection_settings["ahead_light"] = copy.copy(self.light_config["ahead"])
        intersection_settings["ahead_light_time"] = copy.copy(self.light_config["ahead_time"])
        
        return intersection_settings
    
    def import_settings(self,intersection_settings):
        '''
        

        Parameters
        ----------
        intersection_settings : ConfigObj
            the intersection settings we want to import

        Returns
        -------
        new_intersection_setting : ConfigObj
            settings of the intersection
            this will be generated by call self.export_settings() after finishing import
            output these settings are for the purpose of creating the front-end gui
        '''
        
        # remove all vehicle in this intersection 
        # if any vehicle has been added
        for ii in range(len(self.subject_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.subject_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
        
        for ii in range(len(self.left_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.left_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
            
        for ii in range(len(self.right_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.right_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
            
        for ii in range(len(self.ahead_vehicle) - 1, -1, -1): # go through the array in reverse order
            uniquename = self.ahead_vehicle[ii]['uniquename']
            self.remove_vehicle(uniquename)
        
        # import all settings
       
        
        for vehicle_config in intersection_settings["subject_vehicle"]:
            # add vehicles according to imported settings
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'] )
            
        for vehicle_config in intersection_settings["left_vehicle"]:
            # add vehicles according to imported settings
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'] )
            
        for vehicle_config in intersection_settings["right_vehicle"]:
            # add vehicles according to imported settings
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'] )
            
        for vehicle_config in intersection_settings["ahead_vehicle"]:
            # add vehicles according to imported settings
            self.add_vehicle(gap = vehicle_config["gap"], 
                             model_name = vehicle_config["model"], 
                             choice = vehicle_config['choice'], 
                             command = vehicle_config['command'],
                             stop_choice = vehicle_config['stop_choice'],
                             penetrate_distance = vehicle_config['penetrate_distance'],
                             obey_traffic_lights = vehicle_config['obey_traffic_lights'],
                             run = vehicle_config['run'],
                             safety_distance = vehicle_config['safety_distance'] )
    
        self.light_config['subject'] = intersection_settings['subject_light']
        self.light_config['subject_time'] = intersection_settings['subject_light_time']
        
        self.light_config['left'] = intersection_settings['left_light']
        self.light_config['left_time'] = intersection_settings['left_light_time']
        
        self.light_config['right'] = intersection_settings['right_light']
        self.light_config['right_time'] = intersection_settings['right_light_time']
        
        self.light_config['ahead'] = intersection_settings['ahead_light']
        self.light_config['ahead_time'] = intersection_settings['ahead_light_time']
        
        new_intersection_setting = self.export_settings()
        return new_intersection_setting
    

    def _copy_vehicle_settings(self,vehicle_config):
        new_vehicle = copy.copy(vehicle_config)
            
        new_vehicle["ref_waypoint"] = None
        new_vehicle["location"] = None
        new_vehicle["rotation"] = None
        new_vehicle["trajectory"] = None
        new_vehicle["ref_speed_list"] = None
        new_vehicle["stop_ref_point"] = None
        new_vehicle["bounding_box"] = None
        
        return new_vehicle


        
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
        spectator.set_transform(carla.Transform(carla.Location(x=-133.0, y=1.29, z=11.0), carla.Rotation(pitch=-31.0, yaw= -4.23, roll=1.595))) # plain ground
        
        env = CARLA_ENV(world) 
        time.sleep(2) # sleep for 2 seconds, wait the initialization to finish
        
        world_pos = (-133.0,0.0)#(25.4,0.0)
        traffic_light_list = get_traffic_lights(world.get_actors())
        intersection1 = Intersection(env, world_pos, traffic_light_list)
        
        
        name1 = intersection1.add_vehicle()
        
        name2 = intersection1.add_vehicle(command = "left")
        name3 = intersection1.add_vehicle(command = "right")
        
        intersection1.add_vehicle(gap = 5,choice = "left")
        intersection1.add_vehicle(gap = 5, choice = "left",command = "left")
        intersection1.add_vehicle(gap = 5,choice = "left",command = "right")
        intersection1.add_vehicle(choice = "right")
        intersection1.add_vehicle(choice = "right",command = "left")
        intersection1.add_vehicle(choice = "right",command = "right")
        intersection1.add_vehicle(choice = "ahead")
        intersection1.add_vehicle(choice = "ahead",command = "left")
        intersection1.add_vehicle(choice = "ahead",command = "right")
        
        time.sleep(2)
        
        # check the remove method
        intersection1.remove_vehicle(name1)
        intersection1.remove_vehicle(name3)
        intersection1.remove_vehicle(name2)
        
        # traffic light
        intersection1.edit_traffic_light("subject",red_start = 20.0,red_end = 40.0,yellow_start=0.0,yellow_end=20.0,green_start=40.0,green_end = 60.0)
        intersection1.edit_traffic_light("left",red_start = 20.0,red_end = 40.0,yellow_start=0.0,yellow_end=20.0,green_start=40.0,green_end = 60.0)
        intersection1.edit_traffic_light("right",red_start = 20.0,red_end = 40.0,yellow_start=0.0,yellow_end=20.0,green_start=40.0,green_end = 60.0)
        intersection1.edit_traffic_light("ahead",red_start = 20.0,red_end = 40.0,yellow_start=0.0,yellow_end=20.0,green_start=40.0,green_end = 60.0)
        
        # check the import/export method
        setting = intersection1.export_settings()
        
        setting.filename = 'demo_setting1'
        setting.write() # write the setting to file
        
        new_setting = ConfigObj(infile = 'demo_setting1')
        
        intersection1.import_settings(new_setting)
        
        
        for ii in range(int(60 / env.delta_seconds)):
            env.world.tick()
            intersection1.set_intersection_traffic_lights()
        
        
    finally:
        #time.sleep(10)
        env.destroy_actors()

if __name__ == '__main__':
    main()
    
    
