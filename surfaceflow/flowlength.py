import numpy as np
import nibabel as nb

import time

import trimeshpy
from trimeshpy.trimeshflow_vtk import TriMeshFlow_Vtk
from trimeshpy.vtk_util import lines_to_vtk_polydata, save_polydata

def flowlengths(flow):

    diff = flow[1:,:,:] - flow[:-1,:,:]
    steplengths = np.sqrt((diff**2).sum(2))
    linelengths = steplengths.sum(0)

    return linelengths

def compute_flow(vertices, triangles, steps=10, timestep=5):

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
