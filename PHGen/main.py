import numpy as np
import os
import sys

import param as par
import pdiagram as pd


def readcats(fname, cat):
    # if cat == "quijote":
    #     vec = np.genfromtxt(fname, delimiter="\t")
    #     vec = vec[:, [3, 0, 1, 2]]
    # if cat == "molino":
    #     vec = np.genfromtxt(fname)
    #     vec = vec[:, [13, 0, 1, 2]]  # [host halo mass, x, y, z]
    # if cat == "sancho":
    #     vec = np.load(fname)
    #     vec = vec['pos']
    #     vec = np.concatenate((np.array([np.ones(vec.shape[0])]).T, vec), axis=1)  # [1, x, y, z]
    if cat == "flowpm":
        vec = np.load(fname)
        vec = vec[:,[3,4,5]]
        vec = np.concatenate((np.array([np.ones(vec.shape[0])]).T, vec), axis=1)  # [1, x, y, z]

    return vec  # vec = [mass, x, y, z]


def main(arg_hfile, arg_savePrefix, arg_k_):
    # if arg_pd:
    dat = readcats(arg_hfile, par.cat)  # Read halos file
    dat = dat[(dat[:, 0] > par.mmin) & (dat[:, 0] < par.mmax)]  # Delete out-of-range halos
    pd.DIAG(dat=dat, savePrefix=arg_savePrefix, k_=arg_k_)  # Make stuff
    
    # if arg_pi:
    #     pi.IMAG(cut=arg_cut, npool=arg_npool, outfile=arg_pdfile, onedim=arg_onedim, boundsName=arg_boundsName, extremeBounds=arg_extremeBounds, savePrefix=arg_savePrefix, row=arg_row)      


a0      = 0.1       #the initial epoch from where we begin the evolution, a0=0 corresponds to birth but is numerically unstable
af      = 1.0       #final epoch where we visualize structures, af=1 corresponds to today
n_steps = 10        #number of time-steps to split the total evolution into
L       = 256       #Physical size of the Universe in Mpc/h
N       = 128        #Number of mesh-points along one axis, size of the cube. Then the number of particles will be N^3
batch   = 1         #Batch size, how many independent Universes to simulate

# Script
om_input = sys.argv[1]
s8_input = sys.argv[2]
arg_k_ = int(sys.argv[3])

# Run main()
arg_savePrefix = "/staging/hyip2/TDAflow/PHGen/PD/fs_{}_{}_{}_{}_{}_{}_{}_{}_{}".format(a0, af, n_steps, L, N, batch, om_input, s8_input, arg_k_)

arg_hfile = "/staging/hyip2/TDAflow/haloGen/halos/fs_{}_{}_{}_{}_{}_{}_{}_{}.npy".format(a0, af, n_steps, L, N, batch, om_input, s8_input)
# arg_pdfile = ""

# arg_arrayjob = False  # [useless]
# arg_npool = 1  # Processors. For parmap [useless]
# arg_cut = 0  # Cut to cycles with death > cut [useless]
# arg_onedim = False  # Not useful [useless]

# arg_N_min = 0
# # arg_boundsName = arg_pdfile.replace(".txt", "_bounds.txt")
# arg_boundsName = ""
# # arg_extremeBounds = "/gpfs/work4/0/einf733/PH-files/jacky-files-boss-cmass/galaxies_pdpiOutputs_noSubsampling_"+str(arg_k_)+"/"+"extremeComBounds.txt"
# arg_extremeBounds = ""

# if not os.path.isfile(arg_extremeBounds):
#     arg_pd = True
# else:
#     # arg_pd = False  # For anomaly method, need to do main twice
#     arg_pd = True  # For template method, since bound file already exists then just do pd->pi once then it's done
# arg_pi = False

# arg_pd = True
# arg_pi = False

main(arg_hfile, arg_savePrefix, arg_k_)
