import socket
import pickle
# import serial
import time
# baudrate=115200
# port='/dev/ttyACM0'
# ser = serial.Serial(port, baudrate, timeout=1)
# ser.flush()
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

HEADERSIZE = 10

import time


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(('10.0.0.45', 5000))
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
def send(joy,left_controller,right_controller):
    """
    sends driving data to robot and recives data back
    """
    
    msg = pickle.dumps({'leftdrive':left_controller,'rightdrive':right_controller})
    
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    # print("a",msg)
    conn.send(msg)  
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
try:
#     full_msg= b''
#     new_msg = True
    while True:
        data=receive()
        print(data['servo1'])
        send(5,5,5)
        print('Moving servo on channel 0, press Ctrl-C to quit...')
        for i in range(5):

            kit.servo[i].angle = data[str("servo"+i)]
        #     time.sleep(1)
        # kit.servo[0].angle = 0
        # time.sleep(1)
        # Move servo on channel O between extremes.
       
#         msg = conn.recv(32)
#         if new_msg:
#             print("new msg len:",msg[:HEADERSIZE])
#             msglen = int(float(msg[:HEADERSIZE]))
#             new_msg = False
#         full_msg += msg
#         if len(full_msg)-HEADERSIZE == msglen:
            
#             data=pickle.loads(full_msg[HEADERSIZE:])
#             leftdrive=str(data['leftdrive'])
#             rightdrive=str(data['rightdrive'])
#             print(leftdrive,rightdrive)
#             # senddata = str(leftdrive+','+rightdrive +'\n').encode()
#             # ser.write(senddata)
#             # while ser.readline() is None:
#             #     time.sleep(.05)
#             send(5,5,5)
            
#             new_msg = True
#             full_msg = b""
            

                
            
            
except KeyboardInterrupt:
        quit()
        exit()
        print("Control+C pressed, shutting down...")