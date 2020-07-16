#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:50:23 2020

@author: shijiliu
"""




import carla
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import time
from scipy.interpolate import UnivariateSpline
import math

import control # the python-control package, install first
from backend.carla_env import CARLA_ENV # self-written class that provides help functions, should be in the same folder

from backend.generate_path_omit_regulation import generate_path # function for auto-path generation
# PI controller constants
KI = 0.02
KP = 0.5

# pure-pursuit model constants
k = 0.1 # coefficient for look ahead
Lfc = 4.0 # look ahead distance
L = 2.88 # wheelbase

# distance between two near way points
waypoint_separation = 4.0
# enable/disable debug mode to draw trajectory points in carla
DEBUG = True

def get_PI_controller(delta_seconds):
    '''
    Effects: create a discrete state-space PI controller
    '''
    num_pi = [KP, KI] # numerator of the PI transfer function (KP*s + KI)
    den_pi = [1.0, 0.01*KI/KP] # denominator of PI transfer function (s + 0.01*KI/KP)

    sys = control.tf(num_pi,den_pi) # get transfer function for PI controller (since the denominator has a small term 0.01*KI/KP, it is actually a lag-compensator)
    sys = control.sample_system(sys, delta_seconds) # discretize the transfer function (from s-domain which is continuous to z-domain)
                                                        #since our simulation is discrete
    sys = control.tf2ss(sys) # transform transfer function into state space.
    return sys

def speed_control(sys, ref_speeds, curr_speeds, init_values):
    '''
    Effects: get the reference speed, current (measured) speed and initial values
             Use the difference 
                               e = ref_speeds - curr_speeds 
             as the input for the PI controller, derive the new throttle

    Parameters
    ----------
    sys : control.ss 
        state space controller 
    ref_speeds : list of float
        the desired speed we need
    curr_speeds : list of float
        the current speed
    init_values : the initial_values of the system
        DESCRIPTION.

    Returns
    -------
    throttle : float type
        DESCRIPTION.

    '''
    U0 = np.array(ref_speeds) - np.array(curr_speeds)
    #print(U0)
    _,y0,x0 = control.forced_response(sys,U = U0,X0 = init_values[0]) # y0 is the next values, x0 is the state evolution
                                                                      # see https://python-control.readthedocs.io/en/0.8.3/generated/control.forced_response.html#control.forced_response 
    init_values.append(x0[-1])
    throttle = y0[-1]
    return throttle, init_values

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
    splines = [UnivariateSpline(distance, coords, k=1, s=.2) for coords in points.T]
    
    alpha = np.linspace(0,1.02, 2 * len(distance))
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

def get_target_index(location_2d, current_forward_speed, trajectory):
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
    
    Lf = k * current_forward_speed + Lfc
    
    while Lf > l0 and (ind + 1) < len(trajectory):
        delta_d = sum((trajectory[ind + 1] - trajectory[ind])**2)**0.5
        l0 += delta_d
        ind += 1
    
    if ind >= len(trajectory) - 1:
        end_trajectory = True
    else:
        end_trajectory = False
        
    return ind, end_trajectory
    

def smooth_trajectory(trajectory):
    '''
    

    Parameters
    ----------
    trajectory : [(float,float),...,(float,float)]
        2d trajectory.

    Returns
    -------
    smoothed_trajectory : [(float,float),...,(float,float)]
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


def pure_pursuit_control(vehicle_pos_2d, current_forward_speed, trajectory, ref_speed_list, prev_index):
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
    index, end_trajectory = get_target_index(location_2d, current_forward_speed, trajectory)
    
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
    
    Lf = k * current_forward_speed + Lfc
    
    delta = math.atan2(2.0 * L * math.sin(alpha) / Lf, 1.0)
    #print("delta == ", delta, "yaw == ", yaw)
    
    current_ref_speed = ref_speed_list[index]
    
    return delta, current_ref_speed, index, end_trajectory

def generate_waypoints(env, start, end, constant_speed):
    '''
    

    Parameters
    ----------
    env : CARLA_ENV
        The simulation environment
    
    start : (float,float)
        2d position of the start point
    
    end : (float,float)
        2d position of destination

    Returns
    -------
    way_points : list
        A list of (way_point, reference_speed) tuple, 
        where way_points is a tuple of floats (x,y), the first point must be the **current point** of the vehicle
              reference speed is the desired speed for the vehicle after this way point and before the next way point
        e.g. [((0.0,0.0),10.0),((0.0,10.0),1.0)]

    '''
    
    # get the waypoint from carla map
    carla_map = env.world.get_map()
    
    start_raw = carla.Location(x = start[0], y = start[1], z = 0.0)
    end_raw = carla.Location(x = end[0], y = end[1], z = 0.0)
    
    start_waypoint = carla_map.get_waypoint(start_raw)
    end_waypoint = carla_map.get_waypoint(end_raw)
    
    trajectory = generate_path(env,start_waypoint, end_waypoint, waypoint_separation = waypoint_separation)
    
    # generate way_points
    way_points = []
    
    for ii in range(len(trajectory) - 1):
        way_points.append((trajectory[ii],constant_speed))
    
    way_points.append((trajectory[-1], 0.0)) # set the speed at destination to be 0
    
    return way_points



    

def pure_pursuit_control_wrapper(env,start,end,model_uniquename, constant_speed):
    '''
    

    Parameters
    ----------
    env : CARLA_ENV
        The simulation environment
    
    start : (float,float)
        2d position of the start point
    
    end : (float,float)
        2d position of destination
    
    model_uniquename : str
        the name of the vehicle we want to control.

    constant_speed : float
        the speed of the vehicle, assume constant
    Returns
    -------
    None.

    '''
    
    # create control system
    sys = get_PI_controller(env.delta_seconds)
    
    # essential storages for the controller to work
    init_values = deque(maxlen = 2) # the state space values of the system. For a control system to be fully functional
                                    # we need to give initial value
    ref_speeds = deque(maxlen = 2) # the reference / target speed
    curr_speeds = deque(maxlen = 2) # the measured speed of the vehicle
    
    if DEBUG: 
        vehicle_pose = deque(maxlen = 2)
    
    
    # storage for the visualize the reference speed, throttle and measured speed.
    speed = []
    throttles = []
    reference_speed = []
    
    # give initial values to storage, assume the car is released at rest, with no initial speed or acceleration
    init_values.append(0) 
    ref_speeds.append(0)
    curr_speeds.append(0)
    
    current_ref_speed = 0
    index = 0
    
    # get waypoints from auto-trajectory generation, with a constant navigation speed
    way_points = generate_waypoints(env, start, end, constant_speed)
    
    
    # interpolate a trajectory based on way_points for the vehicle to follow
    trajectory, ref_speed_list = get_trajectory(way_points)
    
    if DEBUG:
        points_debug, _ = zip(*way_points)
        env.draw_waypoints(trajectory, points_debug) # draw waypoints and expected trajectory
    
    # main control loop
    while True: #loop for applying control
        env.world.tick()
        
        # get vehicle's speed, location and orientation
        curr_speed = env.get_forward_speed(model_uniquename)
        vehicle_pos_2d = env.get_transform_2d(model_uniquename) # the (x,y) location and yaw angle of the vehicle
        speed.append(curr_speed)
        curr_speeds.append(curr_speed)
        
        # draw real trajectory if debug is enabled
        if DEBUG:
            vehicle_pose.append(vehicle_pos_2d[0])
            if len(vehicle_pose) == 2:
                env.draw_real_trajectory(vehicle_pose)
        
        # use pure-pursuit model to get the steer angle (in radius)
        delta, current_ref_speed, index, end_trajectory = pure_pursuit_control(vehicle_pos_2d, curr_speed, trajectory, ref_speed_list, index)
        steer = np.clip(delta,-1.0,1.0)
        ref_speeds.append(current_ref_speed)
        reference_speed.append(current_ref_speed)
        
        # get throttle to get the next reference speed 
        throttle, init_values = speed_control(sys, ref_speeds, curr_speeds, init_values) # get the throttle control based on reference and current speed
        throttle = np.clip(throttle,0,1) # throttle value is [0,1]
        throttles.append(throttle) # for visualization
        
        # check whether we are reaching the destination or not
        if end_trajectory:
            vehicle_control = carla.VehicleControl(throttle = 0.0,steer=steer,brake = 1.0) # immediately stop the car
            env.apply_vehicle_control(model_uniquename, vehicle_control) # apply control to vehicle
            break
        
        
        # apply throttle-steer-brake control
        if curr_speed <= current_ref_speed:
            vehicle_control = carla.VehicleControl(throttle = throttle,steer=steer) 
        else:
            vehicle_control = carla.VehicleControl(throttle = throttle,steer=steer,brake = 0.5)
        env.apply_vehicle_control(model_uniquename, vehicle_control) # apply control to vehicle
        

    
    return throttles, speed, reference_speed

client = carla.Client("localhost",2000)
client.set_timeout(10.0)
world = client.load_world('Town05')

# set the weather
world = client.get_world()
weather = carla.WeatherParameters(
    cloudiness=10.0,
    precipitation=0.0,
    sun_altitude_angle=90.0)
world.set_weather(weather)

# set the spectator position for demo purpose
spectator = world.get_spectator()
spectator.set_transform(carla.Transform(carla.Location(x=0.0, y=0.0, z=20.0), carla.Rotation(pitch=-31.07, yaw= -90.868, roll=1.595))) # plain ground

env = CARLA_ENV(world) 
time.sleep(2) # sleep for 2 seconds, wait the initialization to finish

# spawn a vehicle, here I choose a Tesla model
spawn_point = carla.Transform(carla.Location(x=14.8, y=5.8, z=5.0), carla.Rotation(pitch=0.000000, yaw= 0, roll=0.000000))
model_name = "vehicle.tesla.model3"
model_uniquename = env.spawn_vehicle(model_name,spawn_point) # spawn the model and get the uniquename, the CARLA_ENV class will store the vehicle into vehicle actor list

time.sleep(5)

'''
way_points = [((-277.08,-15.39),20),
              ((-30.08,-15.39),10),
              ((-12.0,-12.0),10),
              (( -9, 0.0),20),
              (( -9, 50),0)
              ]
'''

start = (14.8,5.8)
end = (31.49375, -12.65625)
constant_speed = 10

try:

    throttles, speed, reference_speed = pure_pursuit_control_wrapper(env,start,end,model_uniquename, constant_speed)
    
    fig,a =  plt.subplots(3,1)
    
    #plt.subplot(3,1,1)
    a[0].plot(reference_speed)
    a[0].set_title('reference speed')
    #plt.subplot(3,1,2)
    a[1].plot(throttles)
    a[1].set_title('throttle applied')
    a[2].plot(speed)
    a[2].set_title('measured speed')
    
    
finally:
    env.destroy_actors()