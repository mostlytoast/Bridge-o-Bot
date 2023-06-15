from urdfpy import URDF
import os
import urdfpy
import numpy as np
file_path='C:/Users/tom-s/OneDrive - Wayzata Public Schools/self building 3d prints + robot/python code/robot 6/urdf/robot 6.urdf'
# os.path.isfile
exists = os.path.isfile(file_path)
print(exists)
robot= URDF.load(file_obj=file_path)
# robot= urdfpy.Sphere(5)
#C:/Users/tom-s/Desktop/python code/v2 robot arm - Copy/urdf/v2 robot arm - Copy.urdf
#C:/Users/tom-s/Desktop/python code/v2 robot arm - Copy/urdf/v2 robot arm - Copy.urdf
# robot.show()
# robot.animate()

ct = {
    '1' : [-np.pi / 4, np.pi / 4],
    '2' : [0.0, -np.pi / 2.0],
    '3' : [0.0, np.pi / 2.0]
}
robot.animate(cfg_trajectory=ct)
