import tensorflow as tf
import numpy as np
import sys
import os


om_input = float(sys.argv[1])
s8_input = float(sys.argv[2])

a0      = 0.1       #the initial epoch from where we begin the evolution, a0=0 corresponds to birth but is numerically unstable
af      = 1.0       #final epoch where we visualize structures, af=1 corresponds to today
n_steps = 10        #number of time-steps to split the total evolution into
L       = 256       #Physical size of the Universe in Mpc/h
N       = 64        #Number of mesh-points along one axis, size of the cube. Then the number of particles will be N^3
batch   = 1         #Batch size, how many independent Universes to simulate

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
print(final_state.shape)
saveName = "fs_{}_{}_{}_{}_{}_{}_{}_{}".format(a0, af, n_steps, L, N, batch, om_input, s8_input)
np.save(saveName, final_state)
os.system("mv "+saveName+".npy /staging/hyip2/TDAflow/snapGen/snaps/")
