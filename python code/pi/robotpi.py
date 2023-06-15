""" 
param hostname: ip of pi on bot,
param username: username for pi default is 'pi',
param password: password for pi default is 'raspberry',
param commands: commands that will be sent to pi via ssh,
param tune_<num>: list of tunning parameters for pid change <num> to the number of the pid class ex tune_1 applies to pid1
"""
import sys
import time
import socket

import math
import pickle 
from simple_pid import PID
from scipy.spatial.transform import Rotation as ROT
import pygame

""" lines 16 to 23 and the send funtion adapted from 'Sockets Tutorial with Python 3 part 3 - sending and receiving Python Objects with sockets'
Title: Sockets Tutorial with Python 3 part 3 - sending and receiving Python Objects with sockets
Author: Harrison
Date: Mar 13, 2019
Code version: unknown 
Availability: https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/ """


pygame.init() # Initialize the joysticks.
pygame.joystick.init()

# tune_1=[3.0,2.6, 0.0,1]#last val is the set point
# tune_2=[.67,.36, 0.0,1]
# pid1 = PID(tune_1)
# pid1.sample_time = .01
# pid2 = PID(tune_2)
# pid2.sample_time = .01
pid1 = PID(3.0,2.6, 0.0, setpoint=1)
pid1.sample_time = .01
pid2 = PID(.67,.36, 0.0, setpoint=1)
pid2.sample_time = .01


""" funtion startupvrsys() and function get_controller_ids() code came from 
Title: htc_vive_controller_keypresses.py
Author: awesomebytes
Date: unknown
Code version: unknown
Availability: https://gist.github.com/awesomebytes/75daab3adb62b331f21ecf3a03b3ab46"""

def translate(value, min_input, max_input, min_output, max_output):
    """
    maps the input value to new range and returns the translated value
    """
    return(((value-max_input)/(max_input-min_input))*(max_output-min_output) +max_output)
def constrain(val, min_input, max_input):
    """
    constrains input 'val' to the min 'min_input' and max 'max_input' and returns the constrained value
    """
    value = max(min(max_input, val), min_input)  
    return value  

def find_direction_to_point(currX,currZ,currR,destX,destZ): 
    """
    finds the direction the dest 'destination' point is compared to the robots current point 
    """
    rad=math.atan2(currX-destX,currZ-destZ)
    destR=math.degrees(rad)
    #destR=translate(destR,-180,180,0,360)
    return(destR*-1)
def min_rotation(currR,destR): 
    """
    finds the min amount needed to rotate to face towards the dest 'destination' rotation 
    """
    if destR>=currR:
        turnright=destR-currR
        turnleft=currR+360-destR
    elif destR<currR:
        turnright=360-currR+destR
        turnleft=currR-destR
    else:
        print('e')
    if(turnleft<=turnright):
        rotation=turnleft*-1
    elif(turnleft>turnright):
        rotation=turnright
    else:
        print('ee')     
    return(rotation)
def distance_pid(currX,currZ,currR,destX,destZ):
    """
    calculates pid for velocity 
    """
    max_lim=15
    min_lim=-1*max_lim
    dis=(math.hypot(currX-destX,currZ-destZ))
    deg=find_direction_to_point(currX,currZ,currR,destX,destZ)
    rotation=min_rotation(currR,deg )
    if abs(rotation)>90:
        dis=dis*-1.0           
    pid2.output_limits= (min_lim,max_lim)        
    pid2.setpoint =  0
    turn= 0
    velocity=translate(pid2(dis),min_lim,max_lim,90+max_lim,90-max_lim )
    return(velocity)
def turn_pid(currR,destR):
    """
    calculates pid for turning 
    """
    max_lim=5
    min_lim=-1*max_lim
    # rotation=min_rotation(currR,destR)
    rotation=currR-destR
    velocity= 90
    pid1.output_limits = (min_lim,max_lim) 
    pid1.setpoint = 0
    turn= pid1(rotation)
    return(turn)
