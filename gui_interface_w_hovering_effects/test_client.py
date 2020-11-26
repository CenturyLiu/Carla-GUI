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