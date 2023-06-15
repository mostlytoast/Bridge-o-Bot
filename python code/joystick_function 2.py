import sys
import time
import socket
import math
import pygame
pygame.init() # Initialize the joysticks.
pygame.joystick.init()
def translate(value, leftMin, leftMax, rightMin, rightMax):#remaps values value is the input variable left min and left max will be streched to right min and max
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)       

def constrain(n, minn, maxn):#constrains input 'n' to the min and max
    return max(min(maxn, n), minn) 
class joyaxis:
    def __init__(self):
        self.axis_x=0
        self.axis_y=0
        self.axis_z=0
        self.axis_t=0
        self.event=''
        joystick_count = pygame.joystick.get_count()
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                done = True # Flag that we are done so we exit this loop.
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                self.event='pressed'
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
                self.event='released'
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.axis={
            0:joystick.get_axis(0),
            1:joystick.get_axis(1),
            2:joystick.get_axis(2),
            3:joystick.get_axis(3)    
            }
            self.button = {
                1:joystick.get_button(0),
                2:joystick.get_button(1),
                3:joystick.get_button(2),
                4:joystick.get_button(3),
                # 5:joystick.get_button(4),
                # 5:0,
                # 6:joystick.get_button(5),
                # 7:joystick.get_button(6),
                # 8:joystick.get_button(7),
                # 9:joystick.get_button(8),
                # 10:joystick.get_button(9),
                # 11:joystick.get_button(10),
                # 12:joystick.get_button(11)
            }
def toggle(button_id):
    joy=joyaxis()
    a=joy.button[button_id]
    time.sleep(.01)
    joy=joyaxis()
    if ((joy.button[button_id]==0)and (a==1)):            
        return(-1)
    else:
        return(1)

