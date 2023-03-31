import numpy as np

f = open("om_s8_list.txt", "w")

# Uros
om_s8_min = [0.2, 0.5]
om_s8_max = [0.5, 1.1]

a0      = 0.1       #the initial epoch from where we begin the evolution, a0=0 corresponds to birth but is numerically unstable
z       = 0.5
af      = 1.0 / (1.0 + z)       #final epoch where we visualize structures, af=1 corresponds to today
n_steps = 10        #number of time-steps to split the total evolution into
L       = 256       #Physical size of the Universe in Mpc/h
N       = 160        #Number of mesh-points along one axis, size of the cube. Then the number of particles will be N^3
batch   = 1         #Batch size, how many independent Universes to simulate

n = 2

for i in range(n):
    draw = np.random.uniform(low=om_s8_min, high=om_s8_max)
    f.write("{}, {}, {}, {}, {}, {}, {}, {}\n".format(str(np.round(draw[0], decimals=4)),str(np.round(draw[1], decimals=4)), a0, z, n_steps, L, N, batch))

f.close()
