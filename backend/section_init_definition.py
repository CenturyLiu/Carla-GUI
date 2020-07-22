#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 11:24:10 2020

@author: shijiliu
"""


import sys
sys.path.append("..")

import carla
from backend.carla_env import CARLA_ENV 
import math
import time
import numpy as np
from configobj import ConfigObj
from backend.generate_path_omit_regulation import generate_path
from backend.intersection_definition import smooth_trajectory, get_trajectory
from scipy.interpolate import UnivariateSpline
import copy

from backend.section_definition import Section


# define a class for defining the initial section
# add vehicles is allowed in this section
class InitSection(Section):
    def __init__(self, env, world_waypoint):
        super().__init__(env, world_waypoint)