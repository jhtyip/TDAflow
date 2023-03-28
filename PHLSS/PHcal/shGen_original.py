import numpy as np

k_array = [100, 60, 30, 15, 5, 1]
# subfolders = ["alpha_m/", "alpha_p/", "fiducial/", "fiducial_ZA/", "h_m/", "h_p/", "logM0_m/", "logM0_p/", "logM1_m/", "logM1_p/", "logMmin_m/", "logMmin_p/", "Mnu_p/", "Mnu_pp/", "Mnu_ppp/", "ns_m/", "ns_p/", "Ob2_m/", "Ob2_p/", "Om_m/", "Om_p/", "s8_m/", "s8_p/", "sigma_logM_m/", "sigma_logM_p/", "w_m/", "w_p/"]
subfolders = ["OR_LSS_m/", "OR_LSS_p/", "LC_m/", "LC_p/", "EQ_m/", "EQ_p/"]

for k in k_array:
    for subfolders_item in subfolders:
        f = open("sub_files/sub_PHcal_"+subfolders_item.replace("/", "")+"_"+str(k)+".sub", "w", newline="\n")
        
        f.write(r"universe = vanilla"+"\n")
        f.write(r"log = PHcal_$(subfolder_item_noSlash)_$(firstNum)_$(secondNum)_"+str(k)+".log"+"\n\n")

        f.write(r"executable = exe_PHcal.sh"+"\n")
        f.write(r"arguments = $(subfolder_item_noSlash) $(firstNum) $(secondNum) $(pythonArgv) "+str(k)+"\n")
        f.write(r"output = PHcal_$(subfolder_item_noSlash)_$(firstNum)_$(secondNum)_"+str(k)+".out"+"\n")
        f.write(r"error = PHcal_$(subfolder_item_noSlash)_$(firstNum)_$(secondNum)_"+str(k)+".err"+"\n\n")

        f.write(r"transfer_input_files = fclaux.py, main.py, mainRunner.py, param.py, pdiagram.py, tar_rm_Output.py"+"\n\n")

        f.write(r"requirements = (Target.HasCHTCStaging == true) && (OpSysMajorVer == 8)"+"\n")
        f.write(r"request_cpus = 1"+"\n")
        f.write(r"request_memory = 4GB"+"\n")  # 4
        f.write(r"request_disk = 3GB"+"\n\n")  # 3

        f.write(r"queue subfolder_item_noSlash,firstNum,secondNum,pythonArgv from ./fileLists/fileList_"+subfolders_item.replace("/", "")+r".txt"+"\n")
        
        f.close()

g = open("PHcal_bashSummit.sh", "w", newline="\n")
g.write(r"#!/bin/bash"+"\n")
for k in k_array:
    for subfolders_item in subfolders:
        g.write(r"condor_submit "+"sub_PHcal_"+subfolders_item.replace("/", "")+"_"+str(k)+".sub"+"\n")
g.close()