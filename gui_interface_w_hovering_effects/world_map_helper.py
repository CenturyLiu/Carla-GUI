#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:49:58 2020

@author: shijiliu
"""
import carla
from configobj import ConfigObj

PIXELS_PER_METER = 12
#-------Utils function--------#


def get_world_width(carla_map):
    '''
    

    Parameters
    ----------
    carla_map : carla map
        get this by carla_map = world.get_map()

    Returns
    -------
    world_width : (float, float)
        width of the world.
    world_offset : (float,float)
        left_upper point of the map.

    '''
    
    
    waypoints = carla_map.generate_waypoints(2)
    margin = 50
    max_x = max(waypoints, key=lambda x: x.transform.location.x).transform.location.x + margin
    max_y = max(waypoints, key=lambda x: x.transform.location.y).transform.location.y + margin
    min_x = min(waypoints, key=lambda x: x.transform.location.x).transform.location.x - margin
    min_y = min(waypoints, key=lambda x: x.transform.location.y).transform.location.y - margin
        
    world_width = max(max_x - min_x, max_y - min_y)
    world_offset = (min_x, min_y)
    return world_width, world_offset

def get_parameters(world_width, world_offset, map_width, map_height, side_length):
    '''
    get essential parameters for transformation

    Parameters
    ----------
    world_width : (float, float)
        width of the world. Get by call get_world_width(carla_map)
    world_offset : (float,float)
        left_upper point of the map. Get by call get_world_width(carla_map)
    map_width : int
        user defined map width for display.
    map_height : int
        user defined map height for display. For convenience, keep map_height same as map_width
    side_length : float
        side length of the intersection. see https://carla-gui.readthedocs.io/en/latest/urban_backend_introduction/#intersection

    Returns
    -------
    pixel_per_meter : int
        pixel per meter .
    meter_per_height_pixel : float
        how long a pixel is representing in the height domain.
    meter_per_width_pixel : float
        how long a pixel is representing in the width domain.

    '''
    
    
    width_in_pixels = (1 << 14) - 1
    surface_pixel_per_meter = int(width_in_pixels / world_width)
    if surface_pixel_per_meter > PIXELS_PER_METER:
            surface_pixel_per_meter = PIXELS_PER_METER

    pixel_per_meter = surface_pixel_per_meter
    meter_per_width_pixel = side_length / map_width
    meter_per_height_pixel = side_length / map_height
    return pixel_per_meter, meter_per_height_pixel, meter_per_width_pixel



def pos_to_pixel(intersection_pos, scale = 1, pixels_per_meter = PIXELS_PER_METER, world_offset = (0,0), offset = (0,0)):
    """Converts the world coordinates to pixel coordinates"""
    x = scale * pixels_per_meter * (intersection_pos[0] - world_offset[0])
    y = scale * pixels_per_meter * (intersection_pos[1] - world_offset[1])
    return [int(x - offset[0]), int(y - offset[1])]

def world_to_pixel_width(scale, width, pixels_per_meter = PIXELS_PER_METER):
    """Converts the world units to pixel units"""
    return int(scale * pixels_per_meter * width)




def world_to_local_pixel(self,world_pos, intersection_pos, subsurface_center, meter_per_height_pixel, meter_per_width_pixel):
    '''
    convert the world location to the a pixel in an intersection image

    Parameters
    ----------
    world_pos : (x,y)
        world location of the actor (e.g. a vehicle's world pos).
    intersection_pos : (x,y)
        world location of the center of intersection (e.g. a vehicle's world pos).
    subsurface_center : (u,v)
        The center of the intersection image. e.g. to display a 1280*720 image, subsurface_center == ( 1280/2, 720/2)
    meter_per_height_pixel : float
        how long a pixel is representing in the height domain. Get by using get_parameters()
    meter_per_width_pixel : float
        how long a pixel is representing in the width domain. Get by using get_parameters()

    Returns
    -------
    local_width_pixel : int
        the width coordinate of the transformed point.
    local_height_pixel : int
        the height coordinate of the transformed point.
    (local_width_pixel,local_height_pixel) is the pixel coordinate of the actor inside the intersection image
    '''
    width_diff = (world_pos[0] - intersection_pos[0]) / meter_per_width_pixel # unit: pixel
    height_diff = (world_pos[1] - intersection_pos[1]) / meter_per_height_pixel 
    local_width_pixel = int(width_diff + subsurface_center[0])
    local_height_pixel = int(height_diff + subsurface_center[1])
    return (local_width_pixel,local_height_pixel)

def local_pixel_to_world(self,local_map_pos, intersection_pos, meter_per_height_pixel, meter_per_width_pixel, subsurface_center ):
    '''
    

    Parameters
    ----------
    local_map_pos : (float, float)
        (local_width_pixel,local_height_pixel), the pixel coordinate of the actor inside the intersection image.
    intersection_pos : (x,y)
        world location of the center of intersection (e.g. a vehicle's world pos).
    meter_per_height_pixel : float
        how long a pixel is representing in the height domain. Get by using get_parameters()
    meter_per_width_pixel : float
        how long a pixel is representing in the width domain. Get by using get_parameters()
    subsurface_center : (u,v)
        The center of the intersection image. e.g. to display a 1280*720 image, subsurface_center == ( 1280/2, 720/2)

    Returns
    -------
    world_x : float
        world x location of the actor.
    world_y : float
        world y location of the actor.

    '''
    
    
    # input the position of an actor in terms of local map of the intersection
    # output the global position of the actor
        
    # ** be cautious about the yaw of the map. Here I assume yaw = 0 for simplicity **
    
    

    width_diff = (local_map_pos[0] - subsurface_center[0]) * meter_per_width_pixel # unit: meter
    height_diff = (local_map_pos[1] - subsurface_center[1]) * meter_per_height_pixel
    world_x = width_diff + intersection_pos[0]
    world_y = height_diff + intersection_pos[1]
    return (world_x,world_y)