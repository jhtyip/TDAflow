import numpy as np
import os
import sys

import param as par
import pdiagram as pd


def readcats(fname, cat):
    # if cat == "quijote":
    #     vec = np.genfromtxt(fname, delimiter="\t")
    #     vec = vec[:, [3, 0, 1, 2]]
    # elif cat == "molino":
    #     vec = np.genfromtxt(fname)
    #     vec = vec[:, [13, 0, 1, 2]]  # [host halo mass, x, y, z]
    if cat == "sancho":
        vec = np.load(fname)
        vec = vec['pos']
        vec = np.concatenate((np.array([np.ones(vec.shape[0])]).T, vec), axis=1)  # [1, x, y, z]

    return vec  # vec = [mass, x, y, z]


def main(arg_hfile, arg_pdfile, arg_pd, arg_npool, arg_pi, arg_cut, arg_onedim, arg_boundsName, arg_N_min, arg_extremeBounds, arg_savePrefix, arg_k_):
    # if arg_pd:
    dat = readcats(arg_hfile, par.cat)  # Read halos file
    dat = dat[(dat[:, 0] > par.mmin) & (dat[:, 0] < par.mmax)]  # Delete out-of-range halos
    pd.DIAG(dat=dat, npool=arg_npool, outfile=arg_pdfile, N_min=arg_N_min, savePrefix=arg_savePrefix, k_=arg_k_)  # Make stuff
    
    # if arg_pi:
    #     pi.IMAG(cut=arg_cut, npool=arg_npool, outfile=arg_pdfile, onedim=arg_onedim, boundsName=arg_boundsName, extremeBounds=arg_extremeBounds, savePrefix=arg_savePrefix, row=arg_row)      


# Script
subfolders_item = sys.argv[1]
subfolders_item_1 = sys.argv[2]
subfolders_item_2 = sys.argv[3]
num1 = sys.argv[4]
num2 = sys.argv[5]
num3 = sys.argv[6]
arg_k_ = int(sys.argv[7])
catFolder = sys.argv[8]+"_"+sys.argv[9]+"_"+sys.argv[10]

# Run main()
arg_savePrefix = subfolders_item.replace("/", "")+"_"+num1+"_"+num2+"_"+num3+"_"+str(arg_k_)

arg_hfile = catFolder+"/gpfs/work4/0/einf733/PH-files/jacky-files/Galaxies/sancho/"+subfolders_item_1+"/"+subfolders_item_1+"_HOD_"+subfolders_item_2+"_NFW_sample"+num1+"_1Gpc_z0.50_RSD"+num2+"_run"+num3+".npz"                                                            
arg_pdfile = ""

arg_arrayjob = False  # [useless]
arg_npool = 1  # Processors. For parmap [useless]
arg_cut = 0  # Cut to cycles with death > cut [useless]
arg_onedim = False  # Not useful [useless]

N_min_dict = {
    "alpha_m/": 341103,
    "alpha_p/": 341103,
    "fiducial/": 354298,
    "fiducial_ZA/": 352436,
    "h_m/": 350122,
    "h_p/": 350122,
    "logM0_m/": 339306,
    "logM0_p/": 339306,
    "logM1_m/": 337320,
    "logM1_p/": 337320,
    "logMmin_m/": 330496,
    "logMmin_p/": 330496,
    "Mnu_p/": 352436,
    "Mnu_pp/": 352436,
    "Mnu_ppp/": 352436,
    "ns_m/": 347266,
    "ns_p/": 347266,
    "Ob2_m/": 353118,
    "Ob2_p/": 353118,
    "Om_m/": 346194,
    "Om_p/": 346194,
    "s8_m/": 344607,
    "s8_p/": 344607,
    "sigma_logM_m/": 351652,
    "sigma_logM_p/": 351652,
    "w_m/": 350256,
    "w_p/": 350256,
    "OR_LSS_m/": 353564,
    "OR_LSS_p/": 353564,
    "LC_m/": 353865,
    "LC_p/": 353865,
    "EQ_m/": 354235,
    "EQ_p/": 354235
}

# arg_N_min = 0
arg_N_min = int(N_min_dict[subfolders_item])
# arg_boundsName = arg_pdfile.replace(".txt", "_bounds.txt")
arg_boundsName = ""
# arg_extremeBounds = "/gpfs/work4/0/einf733/PH-files/jacky-files-boss-cmass/galaxies_pdpiOutputs_noSubsampling_"+str(arg_k_)+"/"+"extremeComBounds.txt"
arg_extremeBounds = ""

# if not os.path.isfile(arg_extremeBounds):
#     arg_pd = True
# else:
#     # arg_pd = False  # For anomaly method, need to do main twice
#     arg_pd = True  # For template method, since bound file already exists then just do pd->pi once then it's done
# arg_pi = False
arg_pd = True
arg_pi = False

main(arg_hfile, arg_pdfile, arg_pd, arg_npool, arg_pi, arg_cut, arg_onedim, arg_boundsName, arg_N_min, arg_extremeBounds, arg_savePrefix, arg_k_)
