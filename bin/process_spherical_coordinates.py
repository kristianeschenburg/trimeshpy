import sys
sys.path.append('../surfaceflow/')

import argparse

import flows
import nibabel as nb
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', help='Source surface.',
    required=True, type=str)
parser.add_argument('-t', '--target', help='Target surface.',
    required=True, type=str)
parser.add_argument('-o', '--output', help='Ouput CSV file.',
    required=True,type=str)

args = parser.parse_args()

source_mesh = args.source
target_mesh = args.target

# Load source and target surfaces
source_mesh = nb.load(source_mesh)
source_vertices = source_mesh.darrays[0].data

target_mesh = nb.load(target_mesh)
target_vertices = target_mesh.darrays[0].data

_, theta, phi = flows.flow_angle(source_vertices, target_vertices)

data_frame = {'theta': theta, 'phi': phi}
data_frame = pd.DataFrame(data_frame)

data_frame.to_csv(args.output, index=False, header=False, sep='\t')
