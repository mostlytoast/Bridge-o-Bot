from ikpy import chain as ch
import math
# import render_urdf
import numpy as np
# import matplotlib.pyplot
# import matplotlib.animation as animation
# from mpl_toolkits.mplot3d import Axes3D
# ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
import time
import sys
import os
import time
import socket
import math
import pygame
pygame.init() # Initialize the joysticks.
pygame.joystick.init()
data=""
usepi=True 

if usepi:
    import robotpc
def translate(value, leftMin, leftMax, rightMin, rightMax):#remaps values value is the input variable left min and left max will be streched to right min and max
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)       

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
import ikpy.utils.plot as plot_utils
my_chain = ch.Chain.from_urdf_file("C:/Users/tom-s/OneDrive - Wayzata Public Schools/self building 3d prints + robot/python code/fixedlimits/urdf/fixedlimits.urdf")

max=.08
dist=.5

def main():
    while True:   
            
        
        joy=joyaxis()
        
        target_position=[translate(joy.axis[1],-1,1,-dist,dist)*-1,translate(joy.axis[0],-1,1,-dist,dist),translate(joy.axis[2],-1,1,.1,dist)] #0.2543609619140625 away
        orientation_axis = "X"
        target_orientation = [0, 0, 1]
            # target_orientation = np.eye(3)
            # target_orientation = forword[:3, :3]
            # b=my_chain.inverse_kinematics(target_position,    target_orientation=target_orientation,    orientation_mode=orientation_axis)
        b=my_chain.inverse_kinematics(target_position,target_orientation=target_orientation,orientation_mode="all")#
            # my_chain.plot(b, ax)
            # matplotlib.pyplot.show()
            # print(math.degrees(b[0] ) ,",",math.degrees(b[1]),"," ,math.degrees(b[2]),",", math.degrees(b[3]),",", math.degrees(b[4]),"," ,math.degrees(b[5])) #,",", math.degrees(b[6] )

            
            
            # my_chain.plot(b, ax,target=target_position,show=True)
            # animation.FuncAnimation(fig, animate, interval=1000)
            # matplotlib.pyplot.show()
     
        if usepi:
            st=robotpc.receive()

        add=135
        test=target_position
            # print(test,"h",math.degrees(b[0] )+add ,math.degrees(b[1])+add,math.degrees(b[2])+add, math.degrees(b[3])+add, math.degrees(b[4])+add,math.degrees(b[5]) +add,math.degrees(b[6]) +add)
            # print(test)
            # print(my_chain.inverse_kinematics(target_position))
            # print(math.degrees(b[0] )+180 ,math.degrees(b[1])+180,math.degrees(b[2])+180, math.degrees(b[3])+180, math.degrees(b[4])+180,math.degrees(b[5]) +180 )
            # robotpc.send(0,0,translate(joy.axis[0],-1,1,0,270) ,translate(joy.axis[1],-1,1,0,270),translate(joy.axis[2],-1,1,0,270),translate(joy.axis[3],-1,1,0,270))

        inv=1
        # data= {str(str('servo')+str(i+1)):5}
        #str("servo"+str(i+1))
        data={}
        for i in range(6):
            data[(str("servo"+str(i+1)))]=math.degrees(b[i+1] )+add 
        print('here',data)
        # render_urdf.update_preview(data)
        if usepi:
            
            # data={'servo1':translate(joy.axis[0],-1,1,0,270),'servo2':translate(joy.axis[1],-1,1,0,270),'servo3':translate(joy.axis[2],-1,1,0,270),'servo4':translate(joy.axis[3],-1,1,0,270),'servo5':5,'servo6':6}    
            # data={'servo1':135,'servo2':135,'servo3':135,'servo4':135,'servo5':135,'servo6':135}    
            robotpc.send(data)

            # robotpc.send(135,135,135,135,135,135)
            print(target_position,data)


if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("quit") 
        robotpc.robot_ssh.stop
        robotpc.robot_ssh.join
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
