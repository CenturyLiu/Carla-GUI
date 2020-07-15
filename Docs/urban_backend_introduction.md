# Urban Backend Core Concepts

This page introduces the main features and modules in urban backend. Reading this page will give you an idea of how the urban backend is working.

Here is a skeleton image showing the relationship between different components involved in the backend. The introduction below is in the order from top to bottom.

	 - urban simulation environment
	       \   
		  - Init Intersection
		  |        \
		  |         - subject lane
		  |                       \
		  |                           - lead vehicle, ego vehicle, follow vehicle
		  | 
		  |         - left lane
		  |                       \
		  |                           - normal vehicle 1, normal vehicle 2, normal vehicle 3
		  | 
		  |         - right lane
		  |                       \
		  |                           - normal vehicle 1
		  | 
		  |         - opposite lane
		  |                       \
		  |                           - normal vehicle 1
		  | 
		  |         - subject light
		  |         - left light
		  |         - right light
		  |         - opposite light
		  |
		  - Normal Intersection 1
		  | 
		  | 
		  | 
		  - Normal Intersection 2
		  | 
		  | 
		  | 
		  | 
		  - Normal Intersection 3


## Urban simulation environment

The urban simulation environment consists of a series of **Intersections**, as shown in the image below. An **ego vehicle** will go in the direction of the green arrow through each intersection.

![urban sim scenario](img/urban_sim_scenario.PNG)

> The 4-intersection urban simulation scenario created inside [Town05](https://carla.readthedocs.io/en/latest/core_map/) provided by CARLA simulator.  


## Intersection

**Intersection** is the major component for simulation scenario creation. A typical **Intersection** is **defined by** the following parameters:

- localization parameters

       - world location: the (x,y) location of the center of **Intersection** with respect to the CARLA MAP. The center is determined by the average of the 4 traffic lights on the corner of the intersection (green box in the picture below).

       - Side length: determine the coverage of an intersection   

![intersection localization](img/intersection_localization.PNG)

> To locate an intersection, we need 2 parameters: world location and side length

- direction parameter

    - yaw: yaw angle used to determine the direction the ego vehicle will go through the intersection

![intersection direction](img/intersection_direction.PNG)
> yaw can be transform into a direction vector, as shown in the picture

With the help of intersection location and direction parameters, we can split the lanes and traffic lights inside the intersection into 4 parts: subject, left, right, opposite, as shown in the following picture

![intersection lane and light seperation](img/intersection_lane_light.PNG)



## Lane

Vehicles are added to each lane.

