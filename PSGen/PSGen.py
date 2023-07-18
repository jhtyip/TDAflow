import sys
import os
import numpy as np
import MAS_library as MASL
import Pk_library as PKL

om_input = str(np.around(float(sys.argv[1]),decimals=6))
s8_input = str(np.around(float(sys.argv[2]),decimals=6))
a0 = np.around(float(sys.argv[3]),decimals=1)
z = np.around(float(sys.argv[4]),decimals=1)
n_steps = int(float(sys.argv[5]))
L = int(float(sys.argv[6]))
N = int(float(sys.argv[7]))
batch = int(float(sys.argv[8]))
i = int(float(sys.argv[9]))

grid    = 64 ##
BoxSize = L
MAS     = 'PCS'

if om_input == "0.3089" and s8_input == "0.8159":
    sim = "fid"
else:
    sim = "swp"

arg_hfile = "/staging/hyip2/TDAflow/haloGen/halos/fs_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.npy".format(om_input, s8_input, a0, z, n_steps, L, N, batch, sim, i) ##
pos = np.load(arg_hfile)[:,[3,4,5]].astype(np.float32)
nhalos = pos.shape[0]

delta = np.zeros((grid,grid,grid), dtype=np.float32)
MASL.MA(pos, delta, BoxSize, MAS, verbose=True)
delta /= np.mean(delta, dtype=np.float64)
delta -= 1.0

axis = 0
Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads=1, verbose=True)
# k       = Pk.k3D
# Pk0     = Pk.Pk[:,0] # monopole
# Pk2     = Pk.Pk[:,1] # quadrupole
# Pk4     = Pk.Pk[:,2] # hexadecapole
# Pkphase = Pk.Pkphase # power spectrum of the phases
# Nmodes  = Pk.Nmodes3D

nhalos_col = np.zeros(Pk.k3D.shape[0])
nhalos_col[0] = nhalos

os.remove(arg_hfile)
np.save("/staging/hyip2/TDAflow/PSGen/{}/fs_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}.npy".format(grid, om_input, s8_input, a0, z, n_steps, L, N, batch, sim, i), np.array([Pk.k3D, Pk.Pk[:,0], nhalos_col]).T) ##