#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 16:16:43 2020

@author: shijiliu
"""
from configobj import ConfigObj
import copy

def read_intersection_settings(config_filename):
    '''
    read the intersection configuration file 
    and transform it into the config file that we can import

    Parameters
    ----------
    config_filename : TYPE
        DESCRIPTION.

    Returns
    -------
    intersection_settings : ConfigObj
        the valid intersection setting that can be imported by 
        intersections

    '''
    # read in raw config file
    intersection_config_raw = ConfigObj(config_filename)
    
    # create the return config
    intersection_settings = ConfigObj()
    
    # vehicles
    intersection_settings["subject_vehicle"] = []
    intersection_settings["left_vehicle"] = []
    intersection_settings["right_vehicle"] = []
    intersection_settings["ahead_vehicle"] = []
    
    # lights
    intersection_settings["subject_light"] = None
    intersection_settings["subject_light_time"] = {}
        
    intersection_settings["left_light"] = None
    intersection_settings["left_light_time"] = {}
        
    intersection_settings["right_light"] = None
    intersection_settings["right_light_time"] = {}
        
    intersection_settings["ahead_light"] = None
    intersection_settings["ahead_light_time"] = {}
    
    # transform vehicle settings
    for vehicle_config_str in intersection_config_raw['subject_vehicle']:
        intersection_settings["subject_vehicle"].append(transform_vehicle_config(vehicle_config_str))
    
    for vehicle_config_str in intersection_config_raw['left_vehicle']:
        intersection_settings["left_vehicle"].append(transform_vehicle_config(vehicle_config_str))
        
    for vehicle_config_str in intersection_config_raw['right_vehicle']:
        intersection_settings["right_vehicle"].append(transform_vehicle_config(vehicle_config_str))
        
    for vehicle_config_str in intersection_config_raw['ahead_vehicle']:
        intersection_settings["ahead_vehicle"].append(transform_vehicle_config(vehicle_config_str))
    
    # transform light settings
    
    if intersection_config_raw["subject_light"] != 'None':
        intersection_settings["subject_light"] = copy.copy(intersection_config_raw["subject_light"])
    
    if intersection_config_raw["left_light"] != 'None':
        intersection_settings["left_light"] = copy.copy(intersection_config_raw["left_light"])
        
    if intersection_config_raw["right_light"] != 'None':
        intersection_settings["right_light"] = copy.copy(intersection_config_raw["right_light"])
        
    if intersection_config_raw["ahead_light"] != 'None':
        intersection_settings["ahead_light"] = copy.copy(intersection_config_raw["ahead_light"])
    
    # transform light time settings
    if intersection_config_raw["subject_light_time"] != 'None':
        for key in intersection_config_raw["subject_light_time"]:
            intersection_settings["subject_light_time"][key] = float(intersection_config_raw["subject_light_time"][key])
    else:
        intersection_settings["subject_light_time"] = None
        
    if intersection_config_raw["left_light_time"] != 'None':
        for key in intersection_config_raw["left_light_time"]:
            intersection_settings["left_light_time"][key] = float(intersection_config_raw["left_light_time"][key])
    else:
        intersection_settings["left_light_time"] = None
        
    if intersection_config_raw["right_light_time"] != 'None':
        for key in intersection_config_raw["right_light_time"]:
            intersection_settings["right_light_time"][key] = float(intersection_config_raw["right_light_time"][key])
    else:
        intersection_settings["right_light_time"] = None
    
    if intersection_config_raw["ahead_light_time"] != 'None':
        for key in intersection_config_raw["ahead_light_time"]:
            intersection_settings["ahead_light_time"][key] = float(intersection_config_raw["ahead_light_time"][key])
    else:
        intersection_settings["ahead_light_time"] = None
    
    
    return intersection_settings
    
'''
def transform_light_time_settings(light_time_str):
    light_time_config = ConfigObj()
    key_val_pairs = light_time_str.split(",")
    for key_val_pair in key_val_pairs:
        temp = key_val_pair.split(": ")
        key = temp[0].split('\'')[1]
        val = temp[1].split('}')[0]
        light_time_config[key] = float(val)
        
    return light_time_config
'''

def transform_vehicle_config(vehicle_config_str):
    '''
    transform the vehicle config in string form
    to configuration file

    Parameters
    ----------
    vehicle_config_str : str
        vehicle config in string form.

    Returns
    -------
    vehicle_config : ConfigObj
        vehicle configuration file

    '''
    vehicle_config = ConfigObj()
    key_val_pairs = vehicle_config_str.split(",")
    for key_val_pair in key_val_pairs:
        temp = key_val_pair.split(": ")
        key = temp[0].split('\'')[1]
        val = temp[1].split('}')[0]
        if key == 'model':
            vehicle_config[key] = val.split("\'")[1]
        elif key == 'gap':
            vehicle_config[key] = float(val)
        elif key == 'command':
            vehicle_config[key] = val.split("\'")[1]
        elif key == 'obey_traffic_lights':
            vehicle_config[key] = bool(val)
        elif key == 'run':
            vehicle_config[key] = bool(val)
        elif key == 'safety_distance':
            vehicle_config[key] = float(val)
        elif key == 'choice':
            vehicle_config[key] = val.split("\'")[1]
        elif key == 'uniquename':
            vehicle_config[key] = val.split("\'")[1]
        elif key == 'ref_waypoint':
            vehicle_config[key] = None
        elif key == 'location':
            vehicle_config[key] = None
        elif key == 'rotation':
            vehicle_config[key] = None
        elif key == 'trajectory':
            vehicle_config[key] = None
        elif key == 'ref_speed_list':
            vehicle_config[key] = None
        elif key == 'bounding_box':
            vehicle_config[key] = None
        elif key == 'vehicle_type':
            vehicle_config[key] = val.split("\'")[1]
        elif key == 'stop_choice':
            vehicle_config[key] = val.split("\'")[1]
        elif key == 'penetrate_distance':
            if vehicle_config['stop_choice'] == 'penetrate':
                vehicle_config[key] = float(val)
            else:
                vehicle_config[key] = None
        elif key == 'stop_ref_point':
            vehicle_config[key] = None
            
    return vehicle_config

def write_intersection_settings(name, settings):
    settings.filename = name
    settings.write()