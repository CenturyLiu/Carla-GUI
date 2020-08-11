# API for connecting CARLA-GUI to real-world simulator

This page introduces the method for the CARLA-GUI to receive throttle, steer and brake commands from external I.O. devices (e.g. a real-world simulator). 

---
## HumanEgoControlClient

This is the client class providing the interface for connecting the external I.O. device with the CARLA-GUI using [python-socket](https://docs.python.org/3/library/socket.html)

### Method

- **<font color="#7fb800">apply_ego_commands</font>**(<font color="#00a6ed">**self, throttle = 0.0, steer = 0.0, brake = 0.0**</font>)		
   add the ego vehicle to the init section
       - **Parameters**
        - `throttle` : float, optional		
                throttle of the vehicle, within [0.0,1.0]

        - `steer` : float, optional	
               the steer of the vehicle, within [-1.0,1.0]


        - `brake` : string, optional	
                the brake of the vehicle, within [0.0,1.0].

---
## Demo Code Recipe

Here is a short code recipe showing the usage of the client class. The code is also available at [test_client.py](https://github.com/CenturyLiu/Carla-GUI/blob/master/gui_interface/test_client.py)

	#!/usr/bin/env python3
	# -*- coding: utf-8 -*-
	"""
	Created on Tue Aug 11 11:35:37 2020
	@author: shijiliu
	"""


	import sys
	sys.path.append("..")

	from backend.human_ego_control import HumanEgoControlClient

	def main():
	    client = HumanEgoControlClient()
	    for ii in range(1000):
			client.apply_ego_commands(throttle = 0.5 + (ii % 10) * 0.01, steer = 0.0, brake = 0.0)
		
	if __name__ == '__main__':
	    main()


---
## Notification
The code recipe above should be easy to understand and use. Here lists several issues that may occur when you are creating your own project.

- Import issue		
   Here is a skeleton drawing showing the file structure of the CARLA-GUI project

	   	 - CARLA-GUI package
		       \   
			  - gui-interface
			  |    \ 
			  |     test_client.py (code recipe above)
			  |
			  |
			  |
			  - backend
			  |    \
			  |     human_ego_control.py (containing the HumanEgoControlClient class)
			  |
			  - your-package

   Import HumanEgoControlClient class using the method described in the code recipe above will only be <font color="#ff0000">**successful**</font> if the script is put inside the gui-interface package or back-end package or any package in <font color="#ff0000">**parallel**</font> with these packages. If you decide not putting your package in parallel with the backend, please remember to <font color="#ff0000">**download**</font> the [human_ego_control.py](https://github.com/CenturyLiu/Carla-GUI/blob/master/backend/human_ego_control.py) and put it in your own directory. Since we are using socket here, the directory won't affect the usefulness of the code.


  


- Timing issue
   If user choose to drive the ego vehicle, the backend will be waiting for the human command at reach update step. During the waiting time, the whole simulation will be paused. To ensure the simulation to be realistic, please make sure your code is functioning fast enough. (The back-end loop is in theory updating each 0.02s, or 50 Hz.)


---
author: shijiliu

date: 2020-08-11 

email: shijiliu@umich.edu

---
