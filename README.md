# Carla-GUI
GUI tool helping vehicle-human interaction researchers to design and conduct traffic experiments with [CARLA simulator](https://carla.org/).

## Team Member

- [Grant Barry](https://github.com/grantbarry29/Carla-GUI)
- [Shiji Liu](https://github.com/CenturyLiu)
- [Weixin Feng(Targy)](https://github.com/Targy/Carla-GUI)

## Project Purpose

The [CARLA simulator](https://carla.org/) is a powerful open source tool developed to "support development, training, and validation of autonomous driving systems". To properly utilize the powerful function provided by the CARLA simulator, however, users need to have 

   - in depth understanding about the function provided by the simulator
   - basic knowledge about vehicle control
   - basic knowledge about python
   
 Meeting all these requirements is definitely not a easy job for beginner researchers in the field of vehicle-human interaction. To make life **easier** for those researchers, we are here to present our **simple GUI**, which is an interface for users to create and conduct experiments inside the CARLA simulator.
 
 ## Function introduction
 
 Our simulator allows users to create both **urban** and **freeway** simulation scenarios. 
 
 ![gui start page](https://github.com/CenturyLiu/Carla-GUI/blob/master/Docs/img/gui_start_page.png)
 
 > The start page of the gui, with choices for editing both urban(intersection) and freeway simulation scenarios.
 
 ### Urban simulation
 
 The GUI for urban simulation is still under development, documents will soon be available.
 
 Here is a demo of back end function for the Urban GUI:
 
 ![urban add vehicle](https://github.com/CenturyLiu/Carla-GUI/blob/master/Docs/img/intersection_add_vehicle.gif)
 > add vehicles inside the urban simulation environment
 
 ![urban simulation start](https://github.com/CenturyLiu/Carla-GUI/blob/master/Docs/img/intersection_start_in_sim.gif)
 > simulation starts inside the CARLA enviroment
 
 For more information about urban simulation scenario, see [urban back end](https://carla-gui.readthedocs.io/en/latest/urban_backend_introduction/)
 
 To view the full process of creating and conducting an urban simulation, please refer to [urban demo video](https://youtu.be/DvECte5iaRw)
 
 ### Freeway simulation
 
 The GUI for freeway simulation is still under development, documents will soon be available.
 
  Here is a demo of back end function for the Freeway GUI:
 
 ![freeway add vehicle](https://github.com/CenturyLiu/Carla-GUI/blob/master/Docs/img/add_vehicle_demo.gif)
 > add vehicles inside the freeway simulation environment
 
 ![freeway simulation snapshort](https://github.com/CenturyLiu/Carla-GUI/blob/master/Docs/img/distance_demo_first_persom.gif)
 > demo of freeway simulation
 
 For more information about urban simulation scenario, see [freeway back end](https://carla-gui.readthedocs.io/en/latest/freeway_backend_introduction/)

 ## Installation
 
 - step 1: download this repository and put it to your desired location on your device (currently support windows and linux)
 - step 2: follow instructions on [PyQt5 website](https://pypi.org/project/PyQt5/) to install PyQt5, which is the tool we used to create the GUI
 - step 3: follow instructions on [back end installation guide](https://carla-gui.readthedocs.io/en/latest/installation_guide/) to install tools essential for the back end.
 
 ---
 author: shiji liu
 email: shijiliu@umich.edu
