import sys
import numpy as np
# import tarfile

# subfolders = [sys.argv[1]]
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

for subfolders_item in subfolders:
    f = open("fileLists/fileList_"+subfolders_item.replace("/","")+".txt", "w")

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
    # file_array = []
    toBeWritten = ""
    thisJob = ""
    for i in realizations:
        for j in i_hod_array:
            for k in RSD_array:
                thisName = subfolders_item+"__"+param_dict[subfolders_item].split()[0]+"__"+param_dict[subfolders_item].split()[1]+"__"+str(j)+"__"+str(k)+"__"+str(i)
                if thisJob == "":
                    thisJob += thisName
                else:
                    thisJob += "qwerty"+thisName

                # file_array.append("/gpfs/work4/0/einf733/PH-files/jacky-files/Galaxies/sancho/"+param_dict[subfolders_item].split()[0]+"/"+param_dict[subfolders_item].split()[0]+"_HOD_"+param_dict[subfolders_item].split()[1]+"_NFW_sample"+str(j)+"_1Gpc_z0.50_RSD"+str(k)+"_run"+str(i)+".npz")
                counter += 1

                if counter % numEachTar == 0:
                    # archive = "hyip2@snellius.surf.nl:/projects/0/einf733/PH-files/jacky-files-sancho/"+"compressed_cat/"+subfolders_item.replace("/", "")+"_"+str(counter-numEachTar)+"_"+str(counter)+".tar.gz"
                    
                    # if counter != numEachTar:
                    #     f.write("\n"+archive)
                    # else:
                    #     f.write(archive)
                    
                    if counter-numEachTar == 0:
                        f.write(subfolders_item.replace("/", "")+", "+str(counter-numEachTar)+", "+str(counter)+", "+thisJob)
                    else:
                        f.write("\n"+subfolders_item.replace("/", "")+", "+str(counter-numEachTar)+", "+str(counter)+", "+thisJob)

                    # if toBeWritten == "":
                    #     toBeWritten += subfolders_item.replace("/", "")+","+str(counter-numEachTar)+","+str(counter)+"asdfgh"+thisJob
                    # else:
                    #     toBeWritten += " " + subfolders_item.replace("/", "")+","+str(counter-numEachTar)+","+str(counter)+"asdfgh"+thisJob

                    thisJob = ""
                
                #     tar = tarfile.open(archive, "w:gz")
                #     for file in file_array:
                #         tar.add(file)
                #     tar.close()
                #     file_array = []
    # f.write(toBeWritten)
    f.close()
