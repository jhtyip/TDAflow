import numpy as np
import sys

subfolder_array = ["alpha_m/", "alpha_p/", "fiducial/", "fiducial_ZA/", "h_m/", "h_p/", "logM0_m/", "logM0_p/", "logM1_m/", "logM1_p/", "logMmin_m/", "logMmin_p/", "Mnu_p/", "Mnu_pp/", "Mnu_ppp/", "ns_m/", "ns_p/", "Ob2_m/", "Ob2_p/", "Om_m/", "Om_p/", "s8_m/", "s8_p/", "sigma_logM_m/", "sigma_logM_p/", "w_m/", "w_p/", "OR_LSS_m/", "OR_LSS_p/", "LC_m/", "LC_p/", "EQ_m/", "EQ_p/"]

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

for subfolder in subfolder_array:
    if subfolder == "fiducial/":  # 10000*1*1
        i_hod_array = [0]
        realizations = np.arange(500, 10500)
        RSD_array = np.arange(3, 4)
    else:  # 500*5*3
        i_hod_array = np.arange(5)
        realizations = np.arange(0, 500)
        RSD_array = np.arange(1, 4)

    logFileName = "numOfGals_"+subfolder.replace("/", "")+".txt"

    num_array = []
    subfolders_item_1 = param_dict[subfolder].split()[0]
    subfolders_item_2 = param_dict[subfolder].split()[1]

    for RSD in RSD_array:
        for realizations_item in realizations:
            for i_hod_array_item in i_hod_array:
                num1 = str(i_hod_array_item)
                num2 = str(RSD)
                num3 = str(realizations_item)
                arg_hfile = "/gpfs/work4/0/einf733/PH-files/jacky-files/Galaxies/sancho/"+subfolders_item_1+"/"+subfolders_item_1+"_HOD_"+subfolders_item_2+"_NFW_sample"+num1+"_1Gpc_z0.50_RSD"+num2+"_run"+num3+".npz"
                halos = np.load(arg_hfile)
                print(arg_hfile, halos["pos"].shape[0], np.where(halos["gtype"]==1)[0].shape[0], np.where(halos["gtype"]==0)[0].shape[0])

                num_array.append([halos["pos"].shape[0], np.where(halos["gtype"]==1)[0].shape[0], np.where(halos["gtype"]==0)[0].shape[0]])

    np.save(logFileName, np.array(num_array))
