# Installation guide

This page discusses how to install and use the code inside the backend. 

## Install essential python modules
The backend uses the following python modules:

- CARLA   
    Follow instructions on [CARLA document](https://carla.readthedocs.io/en/latest/) to install CARLA simulator

- configobj   
    Follow instructions on [configobj document](https://configobj.readthedocs.io/en/latest/configobj.html) to install configobj
     
- Python-control   
    Follow instructions on [Python-control](https://python-control.readthedocs.io/en/0.8.3/intro.html#) to install Python-control

- scipy   
    Follow instructions on [scipy/installation](https://www.scipy.org/install.html) to install scipy

## Download and test backend code

- Test the backend only

    Download the [GUI Backend](https://github.com/CenturyLiu/Carla-GUI/tree/master/backend) and put it in any directory you like as long as the python command `import carla` works.

    The test file for urban backend is "intersection_backend.py". Open CARLA simulator and run `python intersection_backend.py` to verify the backend has been successfully installed.

    Note: the first time you run the code, the following error may occur:

        RuntimeError: time-out of 10000ms while waiting for the simulator, make sure the simulator is ready and connected to localhost:2000

        UnboundLocalError: local variable 'env' referenced before assignment

    This is because the carla client failed to connect to the carla server. Just run the code again and it should be fine.
