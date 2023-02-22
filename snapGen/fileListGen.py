import numpy as np

f = open("om_s8_list.txt", "w")

# Uros
om_s8_min = [0.2, 0.5]
om_s8_max = [0.5, 1.1]

n = 500

for i in range(n):
    draw = np.random.uniform(low=om_s8_min, high=om_s8_max)
    f.write("{}, {}\n".format(str(np.round(draw[0], decimals=4)),str(np.round(draw[1], decimals=4))))

f.close()
