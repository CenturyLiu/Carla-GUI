# the following two lines are for front end user
import sys
sys.path.append("..")

import carla
import time

from backend.intersection_settings_helper import write_intersection_settings, read_intersection_settings

from backend.carla_env import CARLA_ENV # self-written class that provides help functions
from backend.multiple_vehicle_control import VehicleControl
from backend.initial_intersection import  create_intersections, get_ego_spectator, get_ego_left_spectator
from backend.full_path_vehicle import LeadVehicleControl, FollowVehicleControl

from backend.intersection_definition import get_traffic_lights
from backend.intersection_backend import IntersectionBackend

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


   
        # get traffic light list
        traffic_light_list = get_traffic_lights(world.get_actors())


        # get intersection list
        intersection_list = create_intersections(env, 4, traffic_light_list)
        
        # edit intersection
        # these should be done with the help of the front end gui
        init_intersection = intersection_list[0]
        normal_intersections = intersection_list[1:]
        init_intersection.add_ego_vehicle(safety_distance = 15.0, stop_choice = "abrupt", vehicle_color = '255,255,255')
        init_intersection.add_follow_vehicle(follow_distance = 20.0, stop_choice = "penetrate", penetrate_distance = 2.0)
        init_intersection.add_lead_vehicle(lead_distance = 20.0, stop_choice = "abrupt")
        init_intersection.add_vehicle(choice = "left", stop_choice = "abrupt", vehicle_color = '255,255,255')
        init_intersection.add_vehicle(choice = "right",command="left")
        
        # test edit settings
        name1 = init_intersection.add_vehicle(choice = "ahead",command="left")
        name2 = init_intersection.add_vehicle(choice = "ahead",command = "right")
        
        init_intersection.edit_vehicle_settings(name1, choice = "ahead", vehicle_color = '128,128,128')
        init_intersection.edit_vehicle_settings(name2, choice = "ahead", gap = 15.0, vehicle_color = '128,128,128')
        init_intersection.edit_traffic_light("subject")
        init_intersection.edit_traffic_light("left",red_start = 40.0,red_end = 60.0,yellow_start=30.0,yellow_end=40.0,green_start=0.0,green_end = 30.0)
        init_intersection.edit_traffic_light("right",red_start = 0.0,red_end = 10.0,yellow_start=10.0,yellow_end=20.0,green_start=20.0,green_end = 40.0)
        init_intersection.edit_traffic_light("ahead",red_start = 20.0,red_end = 40.0,yellow_start=10.0,yellow_end=20.0,green_start=0.0,green_end = 10.0)


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
        intersection_list[3].edit_traffic_light("ahead")

        # test import/export
        init_setting = init_intersection.export_settings()

        intersection_list[3].import_settings(init_setting)
        intersection_list[3].add_vehicle(command = "left")
        intersection_list[3].add_vehicle()
        third_setting = intersection_list[3].export_settings()

        write_intersection_settings("third_intersection_setting",third_setting)
        new_third_setting = read_intersection_settings('third_intersection_setting')

        intersection_list[2].import_settings(new_third_setting)




        IntersectionBackend(env,intersection_list)
    finally:
        time.sleep(10)
        env.destroy_actors()

if __name__ == '__main__':
    main()
