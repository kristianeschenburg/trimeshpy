import sys
sys.path.append('../')
sys.path.append('../trimeshpy/')
sys.path.append('../surfaceflow/')

import nibabel as nb
import numpy as np

import scipy.io as sio

import trimeshpy
from trimeshpy.trimeshflow_vtk import TriMeshFlow_Vtk
from trimeshpy.vtk_util import lines_to_vtk_polydata, save_polydata

from flows import flow_lengths, flow_angle
import pandas as pd

from niio import write

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s','--surface',help='Input surface mesh.',
    required=True, type=str)
parser.add_argument('-nb', '--diffusion_steps', help='Number of diffusion steps.',
    required=False, default=10, type=float)

parser.add_argument('-dt','--diffusion_size', help='Diffusion step size.',
    required=False, default=5, type=float)

parser.add_argument('-fg', '--flow_gap', help='Spacing between lines, from which to compute flow angle.',
    required=False, type=int, default=2)

parser.add_argument('-hemi', '--hemisphere', help='Hemisphere being processed.',
    required=False, type=str, default='L', choices=['L','R'])

parser.add_argument('-o','--output_base', help='Output base name.',
    required=True, type=str)

args = parser.parse_args()

# Load surface file
surface = nb.load(args.surface)
vertices = surface.darrays[0].data
triangles = surface.darrays[1].data

# Get diffusion step parameters
nb_step = args.diffusion_steps
nb_size = args.diffusion_size

tri_mesh_flow = TriMeshFlow_Vtk(triangles, vertices)

saved_flow = trimeshpy.data.output_test_flow
saved_fib = trimeshpy.data.output_test_fib

out_base = args.output_base
dat_file = ''.join([out_base,'.lines.dat'])
points = tri_mesh_flow.positive_mass_stiffness_smooth(nb_step, 
        nb_size, flow_file=dat_file)

lines = np.memmap(dat_file, dtype=np.float64, 
                  mode='r', shape=(nb_step, 
                  vertices.shape[0], 
                  vertices.shape[1]))

lines = np.asarray(lines)
L = {'lines': lines}
mat_file = ''.join([out_base,'.lines.mat'])
sio.savemat(file_name=mat_file, mdict=L)

# Compute length of flow lines
flow_lengths = flow_lengths(lines)

# Save lines and line length
outbase = args.output_base

length_file = ''.join([out_base,'.lengths.mat'])
lengths = {'flow_lengths': flow_lengths}
sio.savemat(file_name=length_file, mdict=lengths)

# compute flow angles, and save flow surfaces
flow_gap = args.flow_gap
hemi_map = {'L': 'CortexLeft',
            'R': 'CortexRight'}

for fg in np.arange(lines.shape[0]):

    surface_file = ''.join([out_base,
                    '.Layer.{:}.white.32k_fs_LR.surf.gii'.format(fg)])

    surface_verts = lines[fg, :, :].squeeze().astype('float32')
    write.save_surf(surface_verts, triangles,
    surface_file, hemi_map[args.hemisphere])

    if (fg+flow_gap < lines.shape[0]):

        ufg = fg+flow_gap
        
        r, theta, phi = flow_angle(lines[fg,:,:], lines[ufg,:,:])
        angles = {'theta': theta,
                    'phi': phi}

        angle_file=''.join([out_base,
            '.Angle.Source.{:}.Target.{:}.csv'.format(fg, ufg)])

        angles = pd.DataFrame(angles)
        angles.to_csv(path_or_buf=angle_file,
                      header=False, index=False, sep='\t')
