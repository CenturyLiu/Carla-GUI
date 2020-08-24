---------------------------------------------------------------------------------
                        STRUCTURE OF FREEWAY FRONTEND

contact gbarry@umich.edu for any questions

**home.py**
- Choose freeway
- freeway goes to freeway_window.py  
- may take a second to load as it has to create CARLA environment


**freeway_window.py**
- back to start button opens up 'back_home_pop_up.py'
- start simulation button opens 'start_sim_pop_up.py'
- number of freeway sections ranges [1,7]
- clicking road button generates n number of unique 'edit_section.py' pages where n = number of freeway sections (these are stored in 'section_vector.py')


**edit_section.py**
- add vehicles button opens up 'add_vehicles.py' (there is only one 'add_vehicles.py')
- changing section using Section ID combobox will change freeway section page (the purpose of having multiple pages is so that the user may edit the vehicle behavior settings at each section -- behavior example: lane changing)
- import settings will import all vehicle behavior settings from the chosen freeway section
- clicking on ego vehicle will open up 'edit_vehicle_ego.py' (there is only one 'edit_vehicle_ego.py')


**section_vector.py**
- this file contains the list of all section pages
- index 0 is 'freeway_window.py'
- indices 1 to n are 'edit_section.py' pages (e.g section_vector.page_list[3] == edit section 3)


**edit_vehicle.py**
- there are n * c number of unique 'edit_vehicle.py' pages where n = number of sections and c = number of cars (these are stored as edit_vehicle_list in each 'edit_vehicle.py' page
- allows user to change model, color, and behavioral settings of vehicle
- any changes made will go into effect in CARLA environment when user presses the close button
- changes to model or color will change model and color for all sections
- changes to behavior settings will change the behavior settings for only the current section
- delete button is NOT yet implemented


**edit_vehicle_ego.py**
- there is only one 'edit_vehicle_ego.py' page
- any changes made will go into effect in CARLA environment when user presses the close button
- change color, model, safety distance


**add_vehicles.py**
- there is onle one 'add_vehicles.py' page
- cannot click to edit vehicles on 'add_vehicles.py' page
- add vehicle button opens the same pop up window for both subject and left lane -- 'drop_down_window_add.py'
- back button goes back to whichever 'edit_section.py' the user was at when they clicked the add vehicles button
- back button also copies the map from 'add_vehicles.py' to all sections of 'edit_section.py'


**drop_down_window_add.py**
- allows user to add a vehicle in any lane with gap, model, type, and color


**carla_vehicle_list.py**
- file only to map the names of vehicle choices to the CARLA environment vehicle names


**vehicle.py**
- file contains the vehicle object used in frontend
- clickable object
- all cars on map (including ego) are of type Vehicle as defined in vehicle.py


---------------------------------------------------------------------------------
                                PAGE LAYOUTS
Each .py file defines a custom widget and uses the following layout:

Widget Object:

    Constructor():
      #size and font
      
      #member variables

    InitUI():
        #grid definition

        #visual objects and widgets are created(buttons,labels,dropboxes)

        #grid settings
    

    #data for later use in functions(lists, count values)

    #functions for page control
---------------------------------------------------------------------------------
