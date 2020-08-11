#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:54:49 2020

@author: shijiliu
"""


import socket
import time

class HumanEgoControlServer():
    def __init__(self):
        
        self.command_num = 3 # throttle, steer, brake, in total 3
        
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 50007              # Arbitrary non-privileged port
        
        # create the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        
        # wait until a client is online, start connection with the client
        self.s.listen(1)
        
        
        print("Server initialized")
        
    def get_human_command(self):
        '''
        get the command from user
        the command is a string containting the vehicle throttle, steer and brake
        
        Note: 
            the server will be waiting for the latest command
            

        Returns
        -------
        human_command: list [float,float,float]
            the throttle, steer and brake value

        '''
        conn, addr = self.s.accept()
        with conn:
            
            while True:
                data = conn.recv(32)
                if data:
                    #print("Received ", repr(data))
                    human_command = self._decode_command(data)
                    conn.sendall(b'Command received')
                    conn.close()
                    return human_command
                else:
                    print("Invalid input, waiting for valid commands")
                    
    def _decode_command(self,data):
        data = repr(data)
        splitted_command = data.split(",")
        command = []
        for ii in range(self.command_num):
            val_str = splitted_command[ii].split(":")[1]
            command.append(float(val_str))
        return command
        
    def __del__(self):
        self.s.close()
    
class HumanEgoControlClient():
    def __init__(self):
        self.HOST = ''    # The remote host
        self.PORT = 50007              # The same port as used by the server
        
        # create the client
        # create the server
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.s.connect((self.HOST, self.PORT))
        print("Client Initialized")
        
    def apply_ego_commands(self, throttle = 0.0, steer = 0.0, brake = 0.0):
        '''
        helper function for the user to drive ego vehicle by
        applying throttle, steer and brake value

        Parameters
        ----------
        throttle : float
            throttle of the vehicle, within [0.0,1.0]
        steer : float
            the steer of the vehicle, within [-1.0,1.0]
        brake : float
            the brake of the vehicle, within [0.0,1.0].

        Returns
        -------
        None.

        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        
        # get command string
        command_string = self.encode_ego_commands(throttle, steer, brake)
        s.sendall(command_string.encode())
        data = s.recv(32)
        print("Received ", repr(data))
        s.close()
        return
    
    def encode_ego_commands(self, throttle = 0.0, steer = 0.0, brake = 0.0):
        # encode the commands into a string
        # all float input will be formatted into a 2 digit float
        throttle = format(throttle,'.2f')
        steer = format(steer,'.2f')
        brake = format(brake,'.2f')
        command_string = 't:' + str(throttle) + ',' + 's:' + str(steer) + ',' + 'b:' + str(brake) + ',\n'
        return command_string
    
def main():
    server = HumanEgoControlServer()
    for ii in range(20):
        human_command = server.get_human_command()
        print(human_command)

if __name__ == '__main__':
    main()