"""
=====
Robot
=====

We see a 6-DOF robot arm with visuals.
"""
print(__doc__)
from pytransform3d import transformations as pt

import os
import numpy as np
import matplotlib.pyplot as plt
from pytransform3d.urdf import UrdfTransformManager


BASE_DIR = "C:/Users/tom-s/OneDrive - Wayzata Public Schools/self building 3d prints + robot/python code"
data_dir = BASE_DIR
search_path = "."
while (not os.path.exists(data_dir) and
       os.path.dirname(search_path) != "pytransform3d"):
    search_path = os.path.join(search_path, "..")
    data_dir = os.path.join(search_path, BASE_DIR)

tm = UrdfTransformManager()
a=pt.transform_from_pq(np.hstack( (np.array([0,10,10]), np.array([1,0,0,0]))  ) )
filename = os.path.join(data_dir, "robot 6/urdf/robot 6.urdf")
with open(filename, "r") as f:
    robot_urdf = f.read()
    tm.load_urdf(robot_urdf, mesh_path=data_dir)
# tm.set_joint("2", 0.2 * np.pi)
# tm.set_joint("3", 0.2 * np.pi)
# tm.set_joint("5", 0.1 * np.pi)
# tm.set_joint("6", 0.5 * np.pi)
tm.add_transform("base_link","Empty_Link6",a)
print(tm.get_transform("base_link","Empty_Link6"))

print()
tm.plot_visuals("base_link", ax_s=0.6, alpha=0.7)
plt.show()

# {('base_link/visual_0', 'base_link'): 
# array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]])
#        , 
#        ('base_link/collision_0', 'base_link'): 
# array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link1/visual_0', 'Empty_Link1'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link1/collision_0', 'Empty_Link1'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link2/visual_0', 'Empty_Link2'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link2/collision_0', 'Empty_Link2'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link3/visual_0', 'Empty_Link3'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link3/collision_0', 'Empty_Link3'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link4/visual_0', 'Empty_Link4'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link4/collision_0', 'Empty_Link4'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link5/visual_0', 'Empty_Link5'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link5/collision_0', 'Empty_Link5'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link6/visual_0', 'Empty_Link6'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link6/collision_0', 'Empty_Link6'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('base_link', 'robot 6'): array([[1., 0., 0., 0.],
#        [0., 1., 0., 0.],
#        [0., 0., 1., 0.],
#        [0., 0., 0., 1.]]), ('Empty_Link1', 'base_link'): array([[ 0.93392008,  0.3385923 , -0.11466707,  0.0079224 ],
#        [-0.05801954, -0.17294395, -0.9832213 , -0.073935  ],
#        [-0.35274214,  0.92490305, -0.14187086,  0.077111  ],
#        [ 0.        ,  0.        ,  0.        ,  1.        ]]), ('Empty_Link2', 'Empty_Link1'): array([[-5.84374480e-06, -1.00000000e+00,  2.60198192e-06,
#          0.00000000e+00],
#        [-4.15341148e-01,  6.02139001e-08, -9.09665725e-01,
#          4.36660000e-02],
#        [ 9.09665725e-01, -6.39656451e-06, -4.15341148e-01,
#          0.00000000e+00],
#        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
#          1.00000000e+00]]), ('Empty_Link3', 'Empty_Link2'): array([[-1.65640844e-01,  7.34641021e-06, -9.86186144e-01,
#         -9.00000000e-02],
#        [-1.21686558e-06, -1.00000000e+00, -7.24492796e-06,
#          0.00000000e+00],
#        [-9.86186144e-01,  0.00000000e+00,  1.65640844e-01,
#          0.00000000e+00],
#        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
#          1.00000000e+00]]), ('Empty_Link4', 'Empty_Link3'): array([[ 4.42126876e-01, -2.33496005e-01, -8.66027390e-01,
#          1.05590000e-02],
#        [ 4.66999351e-01,  8.84257658e-01,  2.69529108e-06,
#          1.30000000e-03],
#        [ 7.65790723e-01, -4.04435421e-01,  4.99996559e-01,
#         -6.09630000e-03],
#        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
#          1.00000000e+00]]), ('Empty_Link5', 'Empty_Link4'): array([[-1.00656975e-14,  1.00000000e+00,  8.97141003e-15,
#          0.00000000e+00],
#        [-7.46520268e-01, -1.34834886e-14,  6.65362676e-01,
#          0.00000000e+00],
#        [ 6.65362676e-01,  0.00000000e+00,  7.46520268e-01,
#         -1.19857431e-01],
#        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
#          1.00000000e+00]]), ('Empty_Link6', 'Empty_Link5'): array([[ 1.08600912e-16, -1.00000000e+00, -3.48979194e-15,
#          3.35504826e-04],
#        [-3.11045374e-02, -3.49148134e-15,  9.99516137e-01,
#         -1.30000000e-03],
#        [-9.99516137e-01,  0.00000000e+00, -3.11045374e-02,
#          0.00000000e+00],
#        [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
#          1.00000000e+00]])}