import numpy as np
import os.path

subfolders = ["alpha_m/", "alpha_p/", "fiducial/", "fiducial_ZA/", "h_m/", "h_p/", "logM0_m/", "logM0_p/", "logM1_m/", "logM1_p/", "logMmin_m/", "logMmin_p/", "Mnu_p/", "Mnu_pp/", "Mnu_ppp/", "ns_m/", "ns_p/", "Ob2_m/", "Ob2_p/", "Om_m/", "Om_p/", "s8_m/", "s8_p/", "sigma_logM_m/", "sigma_logM_p/", "w_m/", "w_p/", "OR_LSS_m/", "OR_LSS_p/", "LC_m/", "LC_p/", "EQ_m/", "EQ_p/"]

param_dict = {
    "alpha_m/": "fiducial alpha_m",
    "alpha_p/": "fiducial alpha_p",
    "fiducial/": "fiducial fid",
    "fiducial_ZA/": "fiducial_ZA fid",
    "h_m/": "h_m fid",
    "h_p/": "h_p fid",
    "logM0_m/": "fiducial logM0_m",
    "logM0_p/": "fiducial logM0_p",
    "logM1_m/": "fiducial logM1_m",
    "logM1_p/": "fiducial logM1_p",
    "logMmin_m/": "fiducial logMmin_m",
    "logMmin_p/": "fiducial logMmin_p",
    "Mnu_p/": "Mnu_p fid",
    "Mnu_pp/": "Mnu_pp fid",
    "Mnu_ppp/": "Mnu_ppp fid",
    "ns_m/": "ns_m fid",
    "ns_p/": "ns_p fid",
    "Ob2_m/": "Ob2_m fid",
    "Ob2_p/": "Ob2_p fid",
    "Om_m/": "Om_m fid",
    "Om_p/": "Om_p fid",
    "s8_m/": "s8_m fid",
    "s8_p/": "s8_p fid",
    "sigma_logM_m/": "fiducial sigmalogM_m",
    "sigma_logM_p/": "fiducial sigmalogM_p",
    "w_m/": "w_m fid",
    "w_p/": "w_p fid",
    "OR_LSS_m/": "OR_LSS_m fid",
    "OR_LSS_p/": "OR_LSS_p fid",
    "LC_m/": "LC_m fid",
    "LC_p/": "LC_p fid",
    "EQ_m/": "EQ_m fid",
    "EQ_p/": "EQ_p fid"
}

f = open("outputCheck_missing.txt", "w")
for subfolders_item in subfolders:
    print(subfolders_item)
    if subfolders_item == "fiducial/":  # 10000*1*1
        i_hod_array = [0]
        realizations = np.arange(500, 10500)
        RSD_array = np.arange(3, 4)
    else:  # 500*5*3
        i_hod_array = np.arange(5)
        realizations = np.arange(0, 500)
        RSD_array = np.arange(1, 4)

    numEachTar = 25

    counter = 0
    for i in realizations:
        for j in i_hod_array:
            for k in RSD_array:
                counter += 1

                if counter % numEachTar == 0:
                    # print(counter)
                    for k in [1, 5, 15, 30, 60, 100]:
                        if not os.path.exists("/staging/hyip2/PHcal/"+subfolders_item.replace("/", "")+"_"+str(counter-numEachTar)+"_"+str(counter)+"_"+str(k)+".tar.gz"):
                            print("/staging/hyip2/PHcal/"+subfolders_item.replace("/", "")+"_"+str(counter-numEachTar)+"_"+str(counter)+"_"+str(k)+".tar.gz")
                            f.write(subfolders_item+" "+str(counter-numEachTar)+" "+str(counter)+" "+str(k)+"\n")