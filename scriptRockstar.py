import numpy as np
from datetime import datetime
import sys
import os


def Rockstar_ini(par_file,cosmo,z,run):

    w_file=r"""#Rockstar Halo Finder
#See README for details.
# ./rockstar -c quickstart.cfg <particle file>

FILE_FORMAT ="GADGET2"  # or "ART" or "ASCII"
PARTICLE_MASS = 0       # must specify (in Msun/h) for ART or ASCII

# You should specify cosmology parameters only for ASCII formats
# For GADGET2 and ART, these parameters will be replaced with values from the
# particle data file
SCALE_NOW = 1
h0 = 0.7
Ol = 0.73
Om = 0.27

# For GADGET2, you may need to specify conversion parameters.
# Rockstar's internal units are Mpc/h (lengths) and Msun/h (masses)
GADGET_LENGTH_CONVERSION = 1
GADGET_MASS_CONVERSION = 1e+10

FORCE_RES = 0.005 #Force resolution of simulation, in Mpc/h

OUTBASE = "/home/jcalles/PROJECTS/ENG_project/fastSim/byagox{}/Halos/{}/{}"

MIN_HALO_OUTPUT_SIZE = 20
MIN_HALO_PARTICLES = 20
#MASS_DEFINITION = "200c"
"""
    
    file = open(par_file, "w")
    file.write(w_file.format(cosmo,z,run))
    file.close()


cosmo=sys.argv[1]  #'G','NGL','NGLm',ENG'
#z=sys.argv[2]

numFiles=1

cosmo_dict = {'G':'G', 'NGL':'NGL250','NGLm':'NGLm250','ENG':'ENGm1000'}
z_dict = {'z0':2, 'z1':1, 'z2':0}

start=datetime.now()
start_string = start.strftime("%d/%m/%Y %H:%M:%S")
print("start time :", start_string)

for z in ['z0','z1','z2']:
    for i in range(1,numFiles+1):
        ini_parame="/home/jcalles/PROJECTS/ENG_project/fastSim/byagox%s/parameterfiles/rockstar_%s_run%i_param.cfg"%(cosmo,z,i)
        ifile = "/home/jcalles/PROJECTS/ENG_project/fastSim/byagox%s/CDM/byagox_%s_run%i_00%i"%(cosmo,cosmo_dict[cosmo],i,z_dict[z])
        ofile="/home/jcalles/PROJECTS/ENG_project/fastSim/byagox{}/Halos/{}/{}".format(cosmo,z,i)
        print('\nParamFile: %s'%ini_parame)
        print('Cat file: %s'%ifile)
        print('Output file: %s'%ofile)
        print('CAT: %s, run: %i, redshift: %s'%(cosmo_dict[cosmo],i,z))

        Rockstar_ini(ini_parame,cosmo,z,i)

        os.system('./rockstar -c %s %s'%(ini_parame,ifile))

end=datetime.now()
end_string = end.strftime("%d/%m/%Y %H:%M:%S")
print("end time :", end_string)


    
