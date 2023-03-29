import tensorflow as tf
import numpy as np
import sys
import os


om_input = float(sys.argv[1])
s8_input = float(sys.argv[2])

a0 = float(sys.argv[3])
z = float(sys.argv[4])
n_steps = int(sys.argv[5])
L = int(sys.argv[6])
N = int(sys.argv[7])
batch = int(sys.argv[8])

# a0      = 0.1       #the initial epoch from where we begin the evolution, a0=0 corresponds to birth but is numerically unstable
# z       = 0.5
af      = 1.0 / (1.0 + z)       #final epoch where we visualize structures, af=1 corresponds to today
# n_steps = 10        #number of time-steps to split the total evolution into
# L       = 512       #Physical size of the Universe in Mpc/h
# N       = 256        #Number of mesh-points along one axis, size of the cube. Then the number of particles will be N^3
# batch   = 1         #Batch size, how many independent Universes to simulate

# Notes: Uros uses (n_steps=10, L=512, N=128). Hence, (n_steps=10, L=256, N=64) preserves the resolution/particle density


import flowpm
from flowpm.tfpower import linear_matter_power
from flowpm.tfbackground import cosmo

@tf.function
def simulation(om, s8):
    cosmo['sigma8'] = tf.convert_to_tensor(s8, dtype=tf.float32)
    cosmo['Omega0_m'] = tf.convert_to_tensor(om, dtype=tf.float32)
    
    stages = np.linspace(a0, af, n_steps, endpoint=True) #time-steps for the integration
    
    initial_conditions = flowpm.linear_field(N,          # size of the cube
                                             L,          # Physical size of the cube
                                             lambda k: tf.cast(linear_matter_power(cosmo, k), tf.complex64), # Initial powerspectrum
                                             batch_size=batch)

    # Sample particles
    state = flowpm.lpt_init(initial_conditions, a0)   

    # Evolve particles down to z=0
    final_state = flowpm.nbody(state, stages, N)         

    # Retrieve final density field
    # final_field = flowpm.cic_paint(tf.zeros_like(initial_conditions), final_state[0])
    
    return final_state


final_state = simulation(om_input, s8_input)  # 0.3075, 0.8159
# print(final_state.shape)
# saveName = "fs_{}_{}_{}_{}_{}_{}_{}_{}".format(a0, af, n_steps, L, N, batch, om_input, s8_input)
# np.save(saveName, final_state)
# os.system("mv "+saveName+".npy /staging/hyip2/TDAflow/snapGen/snaps/")


rho_crit = 1.8784723e-26  # h^2 kg m^-3
h = 0.6774
Mpc = 3.0857e22  # m
# G = 6.6743015e-11  # N m^2 kg^-2
# rho_crit = 3*(h*100*1000/Mpc)**2/(8*np.pi*G)
Ms = 1.9884e30  # kg

particle_position_x = final_state[0, 0, :, 0]/N*L/h  # Mpc
particle_position_y = final_state[0, 0, :, 1]/N*L/h
particle_position_z = final_state[0, 0, :, 2]/N*L/h
particle_velocity_x = final_state[1, 0, :, 0]/N*L/h  # Mpc s^-1
particle_velocity_y = final_state[1, 0, :, 1]/N*L/h
particle_velocity_z = final_state[1, 0, :, 2]/N*L/h
particle_mass = np.array([om_input*rho_crit*(L**3)*(Mpc**3)/(N**3)/h/Ms]*(N**3))  # Ms

snap_ASCII = [particle_position_x, particle_position_y, particle_position_z, particle_velocity_x, particle_velocity_y, particle_velocity_z, np.arange(particle_position_x.shape[0])]
snap_ASCII = np.array(snap_ASCII).T

saveName = "fs_{}_{}_{}_{}_{}_{}_{}_{}".format(om_input, s8_input, a0, z, n_steps, L, N, batch)
np.savetxt("{}.ascii".format(saveName), snap_ASCII)

os.system("mv {}.ascii /staging/hyip2/TDAflow/haloGen/snaps/".format(saveName))


def quickstart_cfg(quickstart_cfg_saveName, PARTICLE_MASS, Ol, Om, OUTBASE):
    quickstart_cfg_content = r"""#Rockstar Halo Finder
#Quickstart config file for single-cpu, single snapshot halo finding
#Note that non-periodic boundary conditions are assumed.
#See README for details.

#Once compiled ("make"), run Rockstar as
# ./rockstar -c quickstart.cfg <particle data file>

FILE_FORMAT = "ASCII" # or "ART" or "ASCII" or "TIPSY" or "AREPO"
PARTICLE_MASS = {}       # must specify (in Msun/h) for ART or ASCII

# You should specify cosmology parameters only for ASCII formats
# For GADGET2 and ART, these parameters will be replaced with values from the
# particle data file
SCALE_NOW = 1
h0 = 0.6774
Ol = {}
Om = {}

# For GADGET2, you may need to specify conversion parameters.
# Rockstar's internal units are Mpc/h (lengths) and Msun/h (masses)
#GADGET_LENGTH_CONVERSION = 1
#GADGET_MASS_CONVERSION = 1e+10

# For AREPO / GADGET2 HDF5, you would use the following instead:
# Make sure to compile with "make with_hdf5"!
#AREPO_LENGTH_CONVERSION = 1
#AREPO_MASS_CONVERSION = 1e+10

# For TIPSY, you would use:
#TIPSY_LENGTH_CONVERSION = 10    #Typically, box size in Mpc/h
#TIPSY_VELOCITY_CONVERSION = 1e6 #Conversion from TIPSY units to km/s at z=0

FORCE_RES = 0.005 #Force resolution of simulation, in Mpc/h
IGNORE_PARTICLE_IDS = 1

OUTBASE = {}

# For ascii files, the file format is assumed to be:
# X Y Z VX VY VZ ID
"""

    file = open(quickstart_cfg_saveName, "w")
    file.write(quickstart_cfg_content.format(PARTICLE_MASS, Ol, Om, OUTBASE))
    file.close()


quickstart_cfg_saveName = "/staging/hyip2/TDAflow/haloGen/cfgs/quickstart_{}.cfg".format(saveName)
OUTBASE = "/staging/hyip2/TDAflow/haloGen/cfgs/{}".format(saveName)
os.system("mkdir {}".format(OUTBASE))
quickstart_cfg(quickstart_cfg_saveName, particle_mass[0]*h, 1 - om_input, om_input, OUTBASE)

os.system("/staging/hyip2/TDAflow/haloGen/rockstar/rockstar -c {} {}".format(quickstart_cfg_saveName, "/staging/hyip2/TDAflow/haloGen/snaps/{}.ascii".format(saveName)))
halo = np.genfromtxt("{}/halos_0.0.ascii".format(OUTBASE))
np.save("/staging/hyip2/TDAflow/haloGen/halos/{}".format(saveName), halo[:, [1,2,4,8,9,10]])  # [num_p,mvir,rvir,x,y,z]

os.system("rm /staging/hyip2/TDAflow/haloGen/snaps/{}.ascii".format(saveName))
os.system("rm {}".format(quickstart_cfg_saveName))
os.system("rm -r {}".format(OUTBASE))
