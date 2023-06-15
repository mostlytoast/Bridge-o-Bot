"""
===========
Render URDF
===========

Use pyrender to show URDF file. You can get pyrender from

    https://github.com/mmatl/pyrender

or from pip. Make sure to run this from the main folder of pytransform3d.
We will load a simple URDF file but the script is able to display other
URDF files, too. Just change the paths at the end of this file.

Read pyrenders readme for a list of commands that you can use to control
the viewer.
"""
import time
from pytransform3d import transformations as pt
try:
    import pyrender as pr
except ImportError:
    print("This example needs 'pyrender'")
    exit(1)
import numpy as np
import trimesh
from pytransform3d import urdf
from pytransform3d.transformations import transform


def show_urdf_transform_manager(tm, frame, collision_objects=False,
                                visuals=False, frames=False, s=1.0):
    """Render URDF file with pyrender.

    Parameters
    ----------
    tm : UrdfTransformManager
        Transformation manager

    frame : str
        Base frame for rendering

    collision_objects : bool, optional (default: False)
        Render collision objects

    visuals : bool, optional (default: False)
        Render visuals

    frames : bool, optional (default: False)
        Render frames

    s : float, optional (default: 1)
        Axis scale
    """
    scene = pr.Scene()
    if collision_objects:
        if hasattr(tm, "collision_objects"):
            _add_objects(scene, tm, tm.collision_objects, frame)
    if visuals:
        if hasattr(tm, "visuals"):
            nodes_dict=_add_objects(scene, tm, tm.visuals, frame)
    if frames:
        for node in tm.nodes:
            _add_frame(scene, tm, node, frame, s)
    v= pr.Viewer(scene, use_raymond_lighting=True,run_in_thread=True)
    # scene.()
    
    return(v,scene,nodes_dict)





def _add_objects(scene, tm, objects, frame):
    node={}
    i=0
    for obj in objects:
        a=obj.show(scene, tm, frame)
        # print(a)
        node[str(obj)]=a
        i=i+1
    # print(node)
    return(node)
        


def _add_frame(scene, tm, from_frame, to_frame, s=1.0):
    axis_mesh = pr.Mesh.from_trimesh(
        trimesh.creation.axis(
            origin_size=s * 0.1, axis_radius=s * 0.05, axis_length=s),
        smooth=False)
    n = pr.node.Node(
        mesh=axis_mesh, matrix=tm.get_transform(from_frame, to_frame),
        scale=np.ones(3) * s)
    scene.add_node(n)


# We modify the shape objects to include a function that renders them


def box_show(self, scene, tm, frame):
    """Render box."""
    A2B = tm.get_transform(self.frame, frame)

    corners = np.array([
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1]
    ])
    corners = (corners - 0.5) * self.size
    corners = transform(
        A2B, np.hstack((corners, np.ones((len(corners), 1)))))[:, :3]

    mesh = trimesh.Trimesh(
        vertices=corners,
        faces=[[0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 0]]).bounding_box

    mesh = pr.Mesh.from_trimesh(mesh)
    scene.add(mesh)


urdf.Box.show = box_show


def sphere_show(self, scene, tm, frame):
    """Render sphere."""
    A2B = tm.get_transform(self.frame, frame)

    center = A2B[:3, 3]
    phi, theta = np.mgrid[0.0:np.pi:100j, 0.0:2.0 * np.pi:100j]
    X = center[0] + self.radius * np.sin(phi) * np.cos(theta)
    Y = center[1] + self.radius * np.sin(phi) * np.sin(theta)
    Z = center[2] + self.radius * np.cos(phi)

    vertices = []
    faces = []
    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            v1 = [X[i, j], Y[i, j], Z[i, j]]
            v2 = [X[i, j + 1], Y[i, j + 1], Z[i, j + 1]]
            v3 = [X[i + 1, j], Y[i + 1, j], Z[i + 1, j]]
            vertices.extend([v1, v2, v3])
            faces.append(list(range(len(vertices) - 3, len(vertices))))
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces).convex_hull

    mesh = pr.Mesh.from_trimesh(mesh)
    scene.add(mesh)


urdf.Sphere.show = sphere_show


def cylinder_show(self, scene, tm, frame):
    """Render cylinder."""
    A2B = tm.get_transform(self.frame, frame)

    axis_start = A2B.dot(np.array([0, 0, -0.5 * self.length, 1]))[:3]
    axis_end = A2B.dot(np.array([0, 0, 0.5 * self.length, 1]))[:3]
    axis = axis_end - axis_start
    axis /= self.length

    not_axis = np.array([1, 0, 0])
    if (axis == not_axis).all():
        not_axis = np.array([0, 1, 0])

    n1 = np.cross(axis, not_axis)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(axis, n1)

    t = np.linspace(0, self.length, 3)
    theta = np.linspace(0, 2 * np.pi, 50)
    t, theta = np.meshgrid(t, theta)
    X, Y, Z = [axis_start[i] + axis[i] * t +
               self.radius * np.sin(theta) * n1[i] +
               self.radius * np.cos(theta) * n2[i] for i in [0, 1, 2]]

    vertices = []
    faces = []
    for i in range(X.shape[0] - 1):
        for j in range(X.shape[1] - 1):
            v1 = [X[i, j], Y[i, j], Z[i, j]]
            v2 = [X[i, j + 1], Y[i, j + 1], Z[i, j + 1]]
            v3 = [X[i + 1, j], Y[i + 1, j], Z[i + 1, j]]
            vertices.extend([v1, v2, v3])
            faces.append(list(range(len(vertices) - 3, len(vertices))))
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces).convex_hull

    mesh = pr.Mesh.from_trimesh(mesh)
    scene.add(mesh)


urdf.Cylinder.show = cylinder_show


def mesh_show(self, scene, tm, frame):
    """Render mesh."""
    if self.mesh_path is None:
        print("No mesh path given")
        return
    A2B = tm.get_transform(self.frame, frame)

    scale = self.scale

    mesh = trimesh.load(self.filename)
    mesh.vertices *= scale

    mesh = pr.Mesh.from_trimesh(mesh)
    thing=pr.Node(mesh=mesh, matrix=A2B)
    self.node=thing
    # scene.add(mesh, pose=A2B)
    scene.add_node(thing)
    return(thing)

urdf.Mesh.show = mesh_show


def mesh_update(self, scene, tm, frame,nodes_dict):
    """Render mesh."""
    if self.mesh_path is None:
        print("No mesh path given")
        return
    A2B = tm.get_transform(self.frame, frame)

    scale = self.scale
    mesh = trimesh.load(self.filename)
    mesh.vertices *= scale

    mesh = pr.Mesh.from_trimesh(mesh)
    scene.set_pose(nodes_dict, pose=A2B)

# print(urdf.Mesh.show)  

urdf.Mesh.update = mesh_update

# Load your own URDF here:
# (this script should be started from the main directory)
# C:\Users\tom-s\OneDrive - Wayzata Public Schools\self building 3d prints + robot\python code\robot 6\urdf
mesh_path = "C:/Users/tom-s/OneDrive - Wayzata Public Schools/self building 3d prints + robot/python code"
filename = "C:/Users/tom-s/OneDrive - Wayzata Public Schools/self building 3d prints + robot/python code/robot 6/urdf/robot 6.urdf"
frame = "base_link"
#[0.0039215087890625, -0.0039215087890625, 0.22343139648437502] {'servo1': 135.97185832710113, 'servo2': 67.7398105306431, 'servo3': 43.3685490321392, 'servo4': 142.24373212407198, 
# 'servo5': 69.19938048799041, 'servo6': 137.98247602917294, 'amount': 6}
tm = urdf.UrdfTransformManager()
with open(filename, "r") as f:
    tm.load_urdf(f.read(), mesh_path=mesh_path)
tm.set_joint("1", 2.3731566178572967019-2.35619)
tm.set_joint("2", 67.7398105306431-2.35619)
tm.set_joint("3", 0.7569239724215515164-2.35619)
tm.set_joint("4", 2.4826214658837248983-2.35619)
tm.set_joint("5", 1.2077570298527571246-2.35619)
tm.set_joint("6", 2.4082485167572453832-2.35619)
# a=pt.transform_from_pq(np.hstack( (np.array([10,10,10]), np.array([1,0,0,0]))  ) )
x=0
# print(tm.visuals)
v,scene,nodes_dict=show_urdf_transform_manager(    tm, frame, visuals=True, collision_objects=False, frames=False, s=0.05)

# print(urdf.Mesh.show)  
# urdf.Mesh.show
# while (x < 3):
def update_preview(data):    
    tm.set_joint("1", data['servo1'])
    tm.set_joint("2", data['servo2'])
    tm.set_joint("3", data['servo3'])
    tm.set_joint("4", data['servo4'])
    tm.set_joint("5", data['servo5'])
    tm.set_joint("6", data['servo6'])
    
    # obj.show(scene, tm, frame)
        # print(type(obj))
        # import pytransform3d
# a=pt.transform_from_pq(np.hstack( (np.array([10,10,10]), np.array([1,0,0,0]))  ) )
    
    v.render_lock.acquire()
    # for nodes in nodes_dict:
        # print(nodes_dict[nodes])
        # scene.set_pose(nodes_dict[nodes],)
        # obj.update(scene, tm, frame,nodes_dict[nodes])
    for obj in tm.visuals:
        # tm.visuals[]
  
        obj.update(scene, tm, frame,nodes_dict[str(obj)])
    # mesh_update(scene,tm,frame)
    # urdf.Mesh.show = mesh_update
    # print(scene.get_nodes())
    # show_urdf_transform_manager(    tm, frame, visuals=True, collision_objects=False, frames=True, s=0.05)
    
    v.render_lock.release()
    