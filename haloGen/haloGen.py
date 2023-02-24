import numpy as np
import sys


fileName = sys.argv[1]
snap = np.load("{}.npy".format(fileName))

# Read from fileName
om = float(fileName.split("_")[7])
L = int(fileName.split("_")[4])  # Mpc/h
N = int(fileName.split("_")[5])

rho_crit = 1.8784723e-26  # h^2 kg m^-3
h = 0.6774
Mpc = 3.0857e22  # m
# G = 6.6743015e-11  # N m^2 kg^-2
# rho_crit = 3*(h*100*1000/Mpc)**2/(8*np.pi*G)
Ms = 1.9884e30  # kg

particle_position_x = snap[0, 0, :, 0]/N*L/h  # Mpc
particle_position_y = snap[0, 0, :, 1]/N*L/h
particle_position_z = snap[0, 0, :, 2]/N*L/h
particle_velocity_x = snap[1, 0, :, 0]/N*L/h  # Mpc s^-1
particle_velocity_y = snap[1, 0, :, 1]/N*L/h
particle_velocity_z = snap[1, 0, :, 2]/N*L/h
particle_mass = np.array([om*rho_crit*(L**3)*(Mpc**3)/(N**3)/h/Ms]*(N**3))  # Ms

data = {
    "particle_position_x": particle_position_x,
    "particle_position_y": particle_position_y,
    "particle_position_z": particle_position_z,
    "particle_velocity_x": particle_velocity_x,
    "particle_velocity_y": particle_velocity_y,
    "particle_velocity_z": particle_velocity_z,
    "particle_mass": particle_mass
}


import yt
# from yt.units import Msun, parsec


bbox = 1.1 * np.array(
    [[min(particle_position_x), max(particle_position_x)], [min(particle_position_y), max(particle_position_y)], [min(particle_position_z), max(particle_position_z)]]
)

ds = yt.load_particles(data, bbox=bbox)  # , length_unit=parsec, mass_unit=Msun, bbox=bbox)


yt.enable_parallelism()
from yt.extensions.astro_analysis.halo_analysis import HaloCatalog


hc = HaloCatalog(
    data_ds=ds,
    finder_method="rockstar",
    finder_kwargs={"num_readers": 1, "num_writers": 1},
)
hc.create()
