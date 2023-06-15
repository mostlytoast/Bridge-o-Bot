import robotpc 
robot.pi_connect=False
# from robotpc import vr
# import openvr
import math

# virtual=robot.vr()
def server_program():

    
    
    # left_id,right_id=virtual.get_robot_controller()
    
    try:       
        while True:   
            if robot.stop== True:
                robot.robot_thread._stop
                quit()
                
         
            joy=robot.joyaxis()
            # left_data=virtual.get_tracking_data(left_id)
            # right_data=virtual.get_tracking_data(right_id)
            # print(joy[1][0])
            left_data=90
            right_data=90
            robot.send(joy,left_data,right_data)
            
            print(robot.receive())

            # destZ=20
            # destX=0
            # destR=robot.find_direction_to_point(data['cam'][0][0],data['cam'][0][2],data['cam'][0][5],destX,destZ)
            # print(data['cam'][0][5],destR)
            # dist=(math.hypot(data['cam'][0][0]-destX,data['cam'][0][2]-destZ))
         
            # rotation=data['cam'][0][5]-destR
            # if data['cam'][0][7]:
            #     velocity=robot.distance_pid(data['cam'][0][0],data['cam'][0][2],data['cam'][0][5],destX,destZ)
            #     turn=robot.turn_pid(data['cam'][0][5],destR)  
            # if data['cam'][0][7]:
            #     if abs(dist)>2 or abs(rotation)>3:
            #         if abs(dist)>2:
            #             velocity=robot.distance_pid(data['cam'][0][0],data['cam'][0][2],data['cam'][0][5],destX,destZ)
            #             if abs(rotation)>3:             
            #                 turn=robot.turn_pid(data['cam'][0][5],destR)    
            #             else:
            #                 turn=0
            #         else:
            #             velocity=90
            #         if abs(rotation)>3:             
            #             turn=robot.turn_pid(data['cam'][0][5],destR)    
            #         else:
            #             turn=0

        
            # leftdrive = robot.constrain(velocity+turn,0,180)
            # rightdrive = robot.constrain(velocity-turn,0,180)
            # robot.send(leftdrive,rightdrive,'true')
            # print(ge.get_tracking_data(right_id)["button_grip"])
            # a=ge.get_waypoints(left_id,5)
            # print(a)
            # j
            # camera,marker,battery=robot.send(leftdrive,rightdrive)
            # # print('a',turn,rightdrive)
            # c=str(battery).split(',')
            # if len(c)>2:
            #     print(float(c[2]))
                
           
    except KeyboardInterrupt:
        print("Control+C pressed, shutting down...")
        robot.robot_thread._stop
        quit()
        exit()
        

    

    robot.conn.close()  # close the connection


if __name__ == '__main__':

    
    server_program()
