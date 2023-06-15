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
import openvr
import math
import pickle 
# from simple_pid import PID
from scipy.spatial.transform import Rotation as ROT
import pygame
import paramiko
import threading
hostname = "10.0.0.147"
username = "pi"
password = "cheese01"
commands = [
    "python3 test.py"
]
stop=False
pi_connect=True
class robot_ssh(threading.Thread):
    
    def __init__(self,  *args, **kwargs):
        super(robot_start(), self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def robot_start():
    # global stop_robot

    time.sleep(2)
    # if stop_robot:
        
    # initialize the SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)

    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    # execute the commands
    for command in commands:
        print("="*50, command, "="*50)
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)
            robot_ssh.stop
            robot_ssh.join
            stop=True
    
if pi_connect:
    robot_thread = threading.Thread() # create a new thread object.
    robot_thread.run = robot_ssh 
    robot_thread.start() # the new thread is created and then is running.
    
    """ lines 16 to 23 and the send funtion adapted from 'Sockets Tutorial with Python 3 part 3 - sending and receiving Python Objects with sockets'
    Title: Sockets Tutorial with Python 3 part 3 - sending and receiving Python Objects with sockets
    Author: Harrison
    Date: Mar 13, 2019
    Code version: unknown 
    Availability: https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/ """

    HEADERSIZE = 10 
    host = socket.gethostname()
    port = 5000 
    print('current address is ',host,'current port is',port)#put this into the client program so it can connect to this one 
    server_socket = socket.socket() 
    server_socket.bind((host, port))  
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))



""" funtion startupvrsys() and function get_controller_ids() code came from 
Title: htc_vive_controller_keypresses.py
Author: awesomebytes
Date: unknown
Code version: unknown
Availability: https://gist.github.com/awesomebytes/75daab3adb62b331f21ecf3a03b3ab46"""

def send(data):
    """
    sends driving data to robot and recives data back
    """
    data['amount']=len(data)
    # servo1,servo2,servo3,servo4,servo5,servo6
    # data={'servo1':servo1,'servo2':servo2,'servo3':servo3,'servo4':servo4,'servo5':servo5,'servo6':servo6}
    msg = pickle.dumps(data)
    
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
  
    conn.send(msg)  


#    data={'servo1':1,'servo2':2,'servo3':3,'servo4':4,'servo5':5,'servo6':6}
    
    # while conn.recv(1) != 'R':
    #     time.sleep(.01)
def receive():
    full_message= b''
    new_message = True
    while True:
        message = conn.recv(32)
        if new_message:
                # print("new msg len:",msg[:HEADERSIZE])
            message_len = int((message[:HEADERSIZE]))
            new_message = False
        
   
        full_message += message
        if len(full_message)-HEADERSIZE == message_len:
                    
            data=pickle.loads(full_message[HEADERSIZE:])
            # print(data['cam'],data['mark'])
            new_message = True
            full_message = b""
            break
    return(data)


# while True:
#     send(5,5,5)
#     a=receive()
#     print(a)
#     time.sleep(.5)