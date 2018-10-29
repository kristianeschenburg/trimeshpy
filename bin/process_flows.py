import sys
sys.path.append('../trimeshpy/', '../surfaceflow/')

import nibabel as nb
import numpy as np
import flows
import scipy.io as sio

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s','--surface',help='Input surface mesh.',
    required=True, type=str)
parser.add_argument('-nb', '--diffusion_steps', help='Number of diffusion steps.',
    required=False, default=10, type=float)
parser.add_argument('-dt','--diffusion_size', help='Diffusion step size.',
    required=False, default=5, type=float)
parser.add_argument('-o','--output_base', help='Output base name.',
    required=True, type=str)

args = parser.parse_args()

# Load surface file
surface = nb.load(args.surface)
vertices = surface.darrays[0].data
triangles = surface.darrays[1].data

# Get diffusion step parameters
nb_steps = args.diffusion_steps
nb_size = args.diffusion_size

# Compute surface flow
flow_lines = flows.flow_trajectories(
    vertices, triangles, nb_steps, nb_size)
# Compute length of flow lines
flow_lengths = flows.flow_lengths(flow_lines)

# Save lines and line length
outbase = args.output_base

lines = {'flow_lines': flow_lines}
sio.savemat(''.join([outbase, '.lines.mat']), lines)

lengths = {'flow_lengths': flow_lengths}
sio.savemat(''.join([outbase, 'lengths.mat']), lengths)
