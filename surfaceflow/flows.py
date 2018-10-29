import sys
sys.path.append('../trimeshpy/')
sys.path.append('../surfaceflow/')

import numpy as np
import nibabel as nb

import time

import trimeshpy
from trimeshpy.trimeshflow_vtk import TriMeshFlow_Vtk
from trimeshpy.vtk_util import lines_to_vtk_polydata, save_polydata

from dipy.core import geometry

def flow_lengths(flow):

    """
    Compute the flow line lengths.

    Parameters:
    - - - - -
    flow: float, array
        coordinates of each flow line, for each vertex
    
    Returns:
    - - - -
    linelengths: float, array
        length of each flow trajectory for each vertex
    """

    diff = flow[1:,:,:] - flow[:-1,:,:]
    steplengths = np.sqrt((diff**2).sum(2))
    linelengths = steplengths.sum(0)

    return linelengths

def flow_trajectories(vertices, triangles, steps=10, timestep=5):

    """
    Compute the positive mass stiffness surface flow of a surface mesh.

    Parameters:
    - - - - -
    vertices: float array
        list of vertices in mesh
    triangles: int array
        list of faces in mesh
    surface_file: string
        surface file on which to compute flow
    steps: int
        number of diffusion steps
    timestep: int
        diffusion time
    """

    # initialize flow object
    tri_mesh_flow = TriMeshFlow_Vtk(triangles, vertices)\
    # compute final flow surface
    points = tri_mesh_flow.positive_mass_stiffness_smooth(steps, timestep, flow_file=None)
    # get flow trajectory for each mesh vertex
    flow_lines = tri_mesh_flow.get_vertices_flow()

    return flow_lines

def flow_angle(source_vertex, target_vertex):

    """
    Compute normalized unit vector step direction between two surfaces.

    Parameters:
    - - - - -
    source_vertex: float, array
        source mesh vertices
    target_vertex: float, array
        target mesh vertices
    """

    mvmt = target_vertex - source_vertex
    mvmt = mvmt / np.linalg.norm(mvmt, axis=1)[:, None]

    x = mvmt[:, 0]
    y = mvmt[:, 1]
    z = mvmt[:, 2]

    [r, theta, phi] = geometry.cart2sphere(x, y, z)

    return r, theta, phi
