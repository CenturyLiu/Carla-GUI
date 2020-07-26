#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 12:11:46 2020

@author: shijiliu
"""
import sys
sys.path.append("..")

import carla
import time

from backend.carla_env import CARLA_ENV
from backend.section_environment import FreewayEnv

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
        
        # create a 14 section environment (support up to 7)
        freewayenv = FreewayEnv(env,7)
        
        # add ego vehicle
        freewayenv.add_ego_vehicle()
        freewayenv.edit_ego_vehicle(vehicle_color = '255,255,255')
        
        # add 2 lead vehicle and 2 follow vehicle
        
        name0 = freewayenv.add_full_path_vehicle(gap = 20.0, vehicle_type = "lead", choice = "subject")
        name1 = freewayenv.add_full_path_vehicle(gap = 20.0, vehicle_type = "lead", choice = "left")
        name2 = freewayenv.add_full_path_vehicle(vehicle_type = "follow", choice = "subject")
        name3 = freewayenv.add_full_path_vehicle(vehicle_type = "follow", choice = "left")
        name4 = freewayenv.add_full_path_vehicle(gap = 20.0, vehicle_type = "lead", choice = "subject")
        name5 = freewayenv.add_full_path_vehicle(vehicle_type = "follow", choice = "subject")
        
        
        
        # adjust the lead and follow vehicle settings in the third section
        freewayenv.edit_normal_section_setting(section_id = 3, vehicle_type = "lead", choice = "subject", vehicle_index = 0,command = "distance")
        freewayenv.edit_normal_section_setting(section_id = 3, vehicle_type = "lead", choice = "left", vehicle_index = 0,command = "distance")
        freewayenv.edit_normal_section_setting(section_id = 3, vehicle_type = "follow", choice = "subject", vehicle_index = 0,command = "distance")
        freewayenv.edit_normal_section_setting(section_id = 3, vehicle_type = "follow", choice = "left", vehicle_index = 0,command = "distance")
        freewayenv.edit_normal_section_setting(section_id = 3, vehicle_type = "lead", choice = "subject", vehicle_index = 1,command = "distance")
        freewayenv.edit_normal_section_setting(section_id = 3, vehicle_type = "follow", choice = "subject", vehicle_index = 1,command = "distance")
        
        # adjust the lead and follow vehicle settings in the fourth section
        freewayenv.edit_normal_section_setting(section_id = 4, vehicle_type = "lead", choice = "subject", vehicle_index = 0,command = "speed", command_start_time = 0.0)
        freewayenv.edit_normal_section_setting(section_id = 4, vehicle_type = "lead", choice = "left", vehicle_index = 0,command = "speed", command_start_time = 0.0)
        freewayenv.edit_normal_section_setting(section_id = 4, vehicle_type = "follow", choice = "subject", vehicle_index = 0,command = "speed", command_start_time = 0.0)
        freewayenv.edit_normal_section_setting(section_id = 4, vehicle_type = "follow", choice = "left", vehicle_index = 0,command = "speed", command_start_time = 0.0)
        freewayenv.edit_normal_section_setting(section_id = 4, vehicle_type = "lead", choice = "subject", vehicle_index = 1,command = "lane")
        freewayenv.edit_normal_section_setting(section_id = 4, vehicle_type = "follow", choice = "subject", vehicle_index = 1,command = "lane")
        
        # adjust the lead and follow vehicle settings in the sixth section
        freewayenv.edit_normal_section_setting(section_id = 6, vehicle_type = "lead", choice = "subject", vehicle_index = 0,command = "lane")
        freewayenv.edit_normal_section_setting(section_id = 6, vehicle_type = "lead", choice = "left", vehicle_index = 0,command = "lane")
        freewayenv.edit_normal_section_setting(section_id = 6, vehicle_type = "follow", choice = "subject", vehicle_index = 0,command = "lane")
        freewayenv.edit_normal_section_setting(section_id = 6, vehicle_type = "follow", choice = "left", vehicle_index = 0,command = "lane")
        freewayenv.edit_normal_section_setting(section_id = 6, vehicle_type = "lead", choice = "subject", vehicle_index = 1,command = "lane")
        freewayenv.edit_normal_section_setting(section_id = 6, vehicle_type = "follow", choice = "subject", vehicle_index = 1,command = "lane")
        
        # test remove vehicle
        #freewayenv.remove_full_path_vehicle(name4)
        
        
        
        # test editing vehicle settings
        #freewayenv.edit_full_path_vehicle_init_setting(name0, gap = 25.0, vehicle_type = "lead", choice = "subject", vehicle_color = '0,0,0')
        #freewayenv.edit_full_path_vehicle_init_setting(name1, gap = 25.0, vehicle_type = "lead", choice = "left", vehicle_color = '255,255,255')
        #freewayenv.edit_full_path_vehicle_init_setting(name2, gap = 25.0, vehicle_type = "follow", choice = "subject", vehicle_color = '0,0,0')
        #freewayenv.edit_full_path_vehicle_init_setting(name3, gap = 25.0, vehicle_type = "follow", choice = "left", vehicle_color = '255,255,255')
        
        
        freewayenv.SectionBackend()
    finally:
        time.sleep(10)
        env.destroy_actors()
        
    
if __name__ == '__main__':
    main()