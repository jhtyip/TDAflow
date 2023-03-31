import numpy as np

subfolders = ["alpha_m/", "alpha_p/", "fiducial/", "fiducial_ZA/", "h_m/", "h_p/", "logM0_m/", "logM0_p/", "logM1_m/", "logM1_p/", "logMmin_m/", "logMmin_p/", "Mnu_p/", "Mnu_pp/", "Mnu_ppp/", "ns_m/", "ns_p/", "Ob2_m/", "Ob2_p/", "Om_m/", "Om_p/", "s8_m/", "s8_p/", "sigma_logM_m/", "sigma_logM_p/", "w_m/", "w_p/", "OR_LSS_m/", "OR_LSS_p/", "LC_m/", "LC_p/", "EQ_m/", "EQ_p/"]

f = open("queueList.txt", "w")
counter = 0
for param in subfolders:
    if counter != 0:
        f.write("\n")
    f.write(param.replace("/",""))
    counter += 1