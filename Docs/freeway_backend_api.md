# Freeway Backend API reference

This reference discusses the APIs the urban backend provides, and offers some examples to help user understand how to use these APIs.

Different from the urban back end, the freeway back end has intergrated the simulation environment creation, simulation scenario creation and simulation start function in a single class called "FreewayEnv". This page will discuss the methods provided by this class. The implementation details is hidden from users.

---

## FreewayEnv

The FreewayEnv class is the container for the freeway simulation environment. Users can initialize simulation environment, add and edit simulation scenarios and start the simulation by using methods provided by this class.

### Instance Variables

- **<font color="#f8805a">number_of_sections</font>**(int) 	
  The number of sections user want to have for a freeway simulation environment.

- **<font color="#f8805a">max_speed</font>**(float) 	
  The maximum speed allowed for the vehicles to navigate inside the simulation environment. Unit: m/s. Default is 30 m/s.

- **<font color="#f8805a">min_speed</font>**(float) 	
  The minimum speed allowed for the vehicles to navigate inside the simulation environment. Unit: m/s. Default is 15 m/s.

    The speed under "speed" mode will be hold as the average of the max_speed and min_speed, i.e. navigation_speed = (max_speed + min_speed) / 2

### Methods

- **<font color="#7fb800">add_ego_vehicle</font>**(<font color="#00a6ed">**self, model_name = "vehicle.tesla.model3", safety_distance = 15.0, vehicle_color = None**</font>)		
   add the ego vehicle to the init section
       - **Parameters**
        - `model_name` : string, optional		
            vehicle model type. The default is "vehicle.tesla.model3".

        - `safety_distance` : float, optional	
            smallest distance between this vehicle and vehicle ahead. Default is 15 meters.


        - `vehicle_color` : string, optional	
            custom string representation of the RGB color of the vehicle. The string should be in the format 'R,G,B', where R,G,B are integer values. For example, blue is represented as (R,G,B) = (47, 210, 231), then the input string should be '47,210,231'. The default is None, meaning using the default color for the vehicle.

       - **Return**
        - `uniquename` : the uniquename of the vehicle		
<font color="#ff0000">**Note: uniquename of ego is used to reference the ego vehicle in the backend. User cannot change the uniquename. If user want to give the vehicle their own name, remember to store the uniquename.**</font>

- **<font color="#7fb800">edit_ego_vehicle</font>**(<font color="#00a6ed">**self, model_name = "vehicle.tesla.model3", safety_distance = 15.0, vehicle_color = None**</font>)		
   edit the ego vehicle settings by delete the original ego vehicle and add a new one
       - **Parameters**
        - `model_name` : string, optional		
            vehicle model type. The default is "vehicle.tesla.model3".

        - `safety_distance` : float, optional	
            smallest distance between this vehicle and vehicle ahead. Default is 15 meters.


        - `vehicle_color` : string, optional	
            custom string representation of the RGB color of the vehicle. The string should be in the format 'R,G,B', where R,G,B are integer values. For example, blue is represented as (R,G,B) = (47, 210, 231), then the input string should be '47,210,231'. The default is None, meaning using the default color for the vehicle.

       - **Return**
        - `uniquename` : the uniquename of the vehicle		
<font color="#ff0000">**Note: uniquename for the ego vehicle will be changed after editting the settings**</font>

- **<font color="#7fb800">add_full_path_vehicle</font>**(<font color="#00a6ed">**self, model_name = "vehicle.tesla.model3", vehicle_type ="lead", choice = "subject", command = "speed", command_start_time = 0.0, gap = 10.0, safety_distance = 15.0, lead_follow_distance = 20.0, vehicle_color = None**</font>)		

       - **Parameters**
        - `model_name` : string, optional		
            vehicle model type. The default is "vehicle.tesla.model3".

        - `vehicle_type` : string, optional		
            Whether a vehicle is a "lead" vehicle or "follow" vehicle. The default is "lead"

        - `choice` : string, optional	
            the lane this vehicle will be added, valid values: "subject", "left",  The default is "subject".	
<font color="#ff0000"> **Note: 1. use " instead of ', 'subject' is invalid. This rule applies to all the string variables.**</font>


        - `command` : string, optional		
            the section based vehicle command, valid values: "speed", "lane", "distance", The default is "speed"


        - `command_start_time` : float, optional	
            local time after which the command will be applied to the vehicle. This time is local, starting when the ego vehicle arrives at the section reference point of a section (for init section, ego vehicle is added at the reference point). The default is 0.0


        - `gap`  : float,optional		
            the distance between a vehicle and its previous one. Default is 10 meter

        - `safety_distance` : float, optional	
            smallest distance between this vehicle and vehicle ahead. Default is 15 meters.

        - `lead_follow_distance` : float, optional	
            The desired constant distance between a vehicle and the ego vehicle when the "distance" command is applied to a vehicle. 

        - `vehicle_color` : string, optional	
            custom string representation of the RGB color of the vehicle. The string should be in the format 'R,G,B', where R,G,B are integer values. For example, blue is represented as (R,G,B) = (47, 210, 231), then the input string should be '47,210,231'. The default is None, meaning using the default color for the vehicle.

    - **Return**
        - `uniquename` : the uniquename of the vehicle		
<font color="#ff0000">**Note: uniquename is used to reference a vehicle in the backend. Please store the uniquename. If users want to give the vehicle their own name, keep that name seperate from the uniquename.**</font>

- **<font color="#7fb800">remove_full_path_vehicle</font>**(<font color="#00a6ed">**self, uniquename**</font>)		
   remove the uniquename specified lead/follow vehicle from the simulation environment
       - **Parameters**
        - `uniquename` : the uniquename of the vehicle
    - **Return**
        - `removed` : whether the vehicle is successfully removed

- **<font color="#7fb800">edit_full_path_vehicle_init_setting</font>**(<font color="#00a6ed">**self, uniquename, vehicle_type, choice, model_name = "vehicle.tesla.model3", command = "speed", command_start_time = 0.0, gap = 10.0, safety_distance = 15.0, lead_follow_distance = 20.0, vehicle_color = None**</font>)		
       edit the settings of a lead/follow vehicle in the init section. <font color="#ff0000"> Note: the vehicle type and lane choice cannot be changed.</font>
       - **Parameters**
        - `uniquename` : the uniquename of the vehicle

        - `vehicle_type` : string, optional		
            Whether a vehicle is a "lead" vehicle or "follow" vehicle. The default is "lead"

        - `choice` : string, optional	
            the lane this vehicle will be added, valid values: "subject", "left",  The default is "subject".	

        - `model_name` : string, optional		
            vehicle model type. The default is "vehicle.tesla.model3".


        - `command` : string, optional		
            the section based vehicle command, valid values: "speed", "lane", "distance", The default is "speed"


        - `command_start_time` : float, optional	
            local time after which the command will be applied to the vehicle. This time is local, starting when the ego vehicle arrives at the section reference point of a section (for init section, ego vehicle is added at the reference point). The default is 0.0


        - `gap`  : float,optional		
            the distance between a vehicle and its previous one. Default is 10 meter

        - `safety_distance` : float, optional	
            smallest distance between this vehicle and vehicle ahead. Default is 15 meters.

        - `lead_follow_distance` : float, optional	
            The desired constant distance between a vehicle and the ego vehicle when the "distance" command is applied to a vehicle. 

        - `vehicle_color` : string, optional	
            custom string representation of the RGB color of the vehicle. The string should be in the format 'R,G,B', where R,G,B are integer values. For example, blue is represented as (R,G,B) = (47, 210, 231), then the input string should be '47,210,231'. The default is None, meaning using the default color for the vehicle.

    - **Return**
        - `new_uniquename` : string, 		
             new uniquename of the vehicle. 		
<font color="#ff0000">**Note: The uniquename of the vehicle is changed after editing its settings, remember to save the settings**</font>


- **<font color="#7fb800">edit_normal_section_setting</font>**(<font color="#00a6ed">**self, section_id, vehicle_type, choice, vehicle_index, command = "speed", command_start_time = 0.0**</font>)		
       edit the commands that will be applied to a lead/follow vehicle in a normal section. The vehicle is specified by its lane choice and index.
       - **Parameters**
        - `section_id` : int 		
            index of the normal section, starting from 2. (The first normal section is the second section).

        - `vehicle_type` : string 		
            Whether a vehicle is a "lead" vehicle or "follow" vehicle. The default is "lead"

        - `choice` : string 	
            the lane this vehicle will be added, valid values: "subject", "left",  The default is "subject".	

        - `vehicle_index` : int 		
            index of the vehicle in the specific lane, starting from 0.

        - `command` : string, optional		
            the section based vehicle command, valid values: "speed", "lane", "distance", The default is "speed"

        - `command_start_time` : float, optional	
            local time after which the command will be applied to the vehicle. This time is local, starting when the ego vehicle arrives at the section reference point of a section (for init section, ego vehicle is added at the reference point). The default is 0.0.

<font color="#ff0000">**Note: uniquename is used to reference a vehicle in the backend. Please store the uniquename. If users want to give the vehicle their own name, keep that name seperate from the uniquename.**</font>

- **<font color="#7fb800">SectionBackend</font>**(<font color="#00a6ed">**self,spectator_mode = None,allow_collision = True, enable_human_control = False**</font>)		
   main function for starting the simulation.

    - `spectator_mode` : string, optional	
What view mode will be used inside the simulation, valid value is "first_person" (i.e. spectator will be fixed at 10 meters after the last full-path vehicle), "human_driving" (spectator will be put at the position of the human driver). The default value is None, i.e. the spectator will not follow the vehicle.

    - `allow_collision` : bool, optional	
whether collision is allowed in during simulation. The default value is True. <font color="#ff0000">**This method is not stable. There's no guarantee that vehicle will not collide if this value is set to be False** </font>

    - `enable_human_control` : bool, optional	
Parameter indicating whether ego vehicle is controlled by human driver. The default value is **False**. If value is True, then human will be responsible for controlling the vehicle. <font color="#ff0000">Note: 1. if value is True, human command is needed. See the human-ego tutorial for more detail. 2. if value is True, the spectator mode will be automatically set to **"human_driving"** no matter what value is entered </font>

- **<font color="#7fb800">get_vehicle_bounding_box</font>**(<font color="#00a6ed">**self, uniquename**</font>)		
    get the bounding box of the vehicle specified by the uniquename

       - **Parameters**
        - `uniquename` : string	
the uniquename of the vehicle

       - **Returns**
        - `new_bb` : carla.Vector3D	
the bounding box of the vehicle. new_bb.x is the length, new_bb.y is the width, new_bb.z is the height


---
## Demo Code Recipe

Here is a demo for using the back end. The code below creates a 7-section environment, adds 3 lead vehicles, 3 follow vehicles and the ego vehicle, edits control to vehicles in section 1, 3, 4, 6 and then starts the simulation. This example is also available at [test_freeway_backend](https://github.com/CenturyLiu/Carla-GUI/blob/master/gui_interface/test_freeway_backend.py)

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
		
			# get bounding box
			bb = freewayenv.get_vehicle_bounding_box(name1)
			print("bb.x = %f, bb.y = %f, bb.z = %f" % (bb.x,bb.y,bb.z)
			
			
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

Note:

    Note: the first time you run the code, the following error may occur:

        RuntimeError: time-out of 10000ms while waiting for the simulator, make sure the simulator is ready and connected to localhost:2000

        UnboundLocalError: local variable 'env' referenced before assignment

    This is because the carla client failed to connect to the carla server. Just run the code again and it should be fine.

---
author: shijiliu

date: 2020-07-26 

email: shijiliu@umich.edu

---

