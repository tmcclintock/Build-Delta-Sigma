import numpy as np

data = np.genfromtxt("xi_hm_z0.0_13.0_13.1.txt.treecorr")

R = data[:,1]
xi_hm = data[:,3]
np.savetxt("R.txt",R)
np.savetxt("xi_hm_z0.0_13.0_13.1.txt",xi_hm)

