# Carla-GUI
GUI tool to help human-vehicle interaction researchers design and conduct traffic experiments with [CARLA real-time driving simulator](https://carla.org/).

## Team Members

- [Grant Barry](https://github.com/grantbarry29/Carla-GUI)
- [Shiji Liu](https://github.com/CenturyLiu)
- [Weixin Feng(Targy)](https://github.com/Targy/Carla-GUI)

## Project Purpose

The [CARLA simulator](https://carla.org/) is a powerful open source tool developed to "support development, training, and validation of autonomous driving systems" ([introduction, CARLA Simulator](https://carla.org/)). To properly utilize the powerful functionality provided by the CARLA simulator, however, users need to have: 

   - an in depth understanding about the function provided by the simulator
   - basic knowledge about vehicle control
   - basic knowledge about python
   
 Meeting all these requirements is definitely not easy for begining researchers in the field of human-vehicle interaction. To make life **easier** for those researchers, a **simple GUI** has been developed, which provides an interface for users to create and conduct experiments using the CARLA simulator.
 
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

 To view the full process of creating and conducting an urban simulation, please refer to [freeway demo video](https://youtu.be/z3-JaiWRf4g)

 ## Installation
 
 - step 1: download this repository and put it to your desired location on your device (currently support windows and linux)
 - step 2: follow instructions on [PyQt5 website](https://pypi.org/project/PyQt5/) to install PyQt5, which is the tool we used to create the GUI
 - step 3: follow instructions on [back end installation guide](https://carla-gui.readthedocs.io/en/latest/installation_guide/) to install tools essential for the back end.
 
 
## Poster
![Poster](https://github.com/CenturyLiu/Carla-GUI/blob/master/Docs/img/poster.PNG)
> The poster briefly describing the project

 ---
 author: shiji liu
 email: shijiliu@umich.edu
