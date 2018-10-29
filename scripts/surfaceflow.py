import argparse
import time

import nibabel as nb
import numpy as np

import trimeshpy
from trimeshpy.trimeshflow_vtk import TriMeshFlow_Vtk
from trimeshpy.vtk_util import lines_to_vtk_polydata, save_polydata

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--surface', help='Input surface file.',
    required=True, type=str)
parser.add_argument('-st', '--surface_type', help='Format of surface file.',
    required=False, default='gifti', type=str, choices=['gifti','freesurfer'])
parser.add_argument('--nb', help='Number of smoothing iterations.',
    required=True, type=int)
parser.add_argument('--ds', help='Number of diffusion steps.',
    required=True, type=int)

args = parser.parse_args()

nb_step = args.nb
diffusion_step = args.ds

# Load surface file
if args.surface_type == 'gifti':
    surface = nb.load(args.surface)
    vertices = surface.darrays[0].data
    triangles = surface.darrays[1].data
else:
    vertices, triangles = nb.freesurfer.io.read_geometry(args.surface)

saved_flow = trimeshpy.data.output_test_flow
saved_fib = trimeshpy.data.output_test_fib

tri_mesh_flow = TriMeshFlow_Vtk(triangles, vertices)

start = time.time()
points = tri_mesh_flow.positive_mass_stiffness_smooth(
    nb_step, diffusion_step, flow_file=saved_flow)
stop = time.time()

print('Total time: {:}'.format(start-stop))
