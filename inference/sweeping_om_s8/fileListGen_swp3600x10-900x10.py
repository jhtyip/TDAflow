import numpy as np

f = open("om_s8_list_swp3600x10-900x10.txt", "w")

# Uros
# om_s8_min = [0.1, 0.6]
# om_s8_max = [0.5, 1.0]

# Sweeping [om_fid=0.3089, s8_fid=0.8159]
# om_s8_min = [0.2589, 0.7659]
# om_s8_max = [0.3589, 0.8659]

om_s8_min = [0.2089, 0.7159]
om_s8_max = [0.4089, 0.9159]

a0      = 0.1       #the initial epoch from where we begin the evolution, a0=0 corresponds to birth but is numerically unstable
z       = 0.5
af      = 1.0 / (1.0 + z)       #final epoch where we visualize structures, af=1 corresponds to today
n_steps = 10        #number of time-steps to split the total evolution into
L       = 256       #Physical size of the Universe in Mpc/h
N       = 160        #Number of mesh-points along one axis, size of the cube. Then the number of particles will be N^3
batch   = 1         #Batch size, how many independent Universes to simulate

n = 10

for x in np.linspace(om_s8_min[0], om_s8_max[0], num=60):
    for y in np.linspace(om_s8_min[1], om_s8_max[1], num=60):
        if x > 0.3589 or x < 0.2589 or y > 0.8659 or y < 0.7659:
            for i in range(n):
                # draw = np.random.uniform(low=om_s8_min, high=om_s8_max)
                draw = [x, y]
                f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(str(np.round(draw[0], decimals=6)),str(np.round(draw[1], decimals=6)), a0, z, n_steps, L, N, batch, i))

f.close()
