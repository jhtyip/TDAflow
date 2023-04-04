# Type of halo catalog. Refer to DataReading.readcatalogs
cat = "sancho"

# BOX SIZE OF THE SIMULATIONS IN MPC/H
box = 1000
# SIZE OF THE SUB-BOXES
smallbox = 1000  # i.e. no sub-box now

# Minimum Mass of Halos
mmin = 0  # Unbounded
# Maximum Mass of Halos
mmax = 1e99  # Unbounded

# Choose method: 0 = alpha filtration, 1 = sublevel filtration, 2 = alpha-DTM filtration, 3 = alpha-DTM with length-DTM mixing
method = 3

# Number of halos per subbox
# nhalo = 352527  # To be determined
# nhalo = 350000

# # Redshift
# z = 2  # What does this do anyway (nothing)