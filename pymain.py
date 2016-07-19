"""
This is an example file of how to interface with the python wrapper
that can run the Build-Delta-Sigma code.

STEP 0: compile with:
make SHARED=yes

NOTE: You will likely have to change the path to the
GSL libraries in the Makefile for your own machine.

This should result in a BuildDeltaSigma.so file.
"""

"""
First, we have to give the path to the Build_Delta_Sigma.py file,
which is located in src/wrapper/

One day I'll figure out how to write a setup.py script and
have it install in the python directory.
"""
import sys
sys.path.insert(0,"src/wrapper/")
import Build_Delta_Sigma
import matplotlib.pyplot as plt
import numpy as np

test_path = "test_data/"

#First load in the halo-matter CF from somewhere
R = np.genfromtxt(test_path+"R.txt")
xi_hm = np.genfromtxt(test_path+"xi_hm_z0.0_13.0_13.1.txt")

#Create a dictionary with the cosmology
cosmo = {"h":0.7,"om":0.3,"ok":0.0,"ode":0.7}
cosmo["ode"]=1.0-cosmo["om"]

"""
Create a dictionary with all starting params. They are:
Mass - mass of the halo
concentration - concentration of the halo
NR - number of radial points you want to sample
delta - overdensity
Rmis - width of the miscentering 2D Gaussian in units of Mpc/h
fmis - fracton of miscentered halos
timing - 1 if you want to print timing information, 0 if not
miscentering - 1 if you want to calculate miscentered information, 0 if not
"""
input_params = {"Mass": 10**13.,"delta":200,"timing":1,\
                    "Rmis":0.2,"fmis":0.3,"miscentering":1}
#input_params["concentration"] = 5.0 #For eduardo's stuff
input_params["concentration"] = 4.0*(input_params["Mass"]/5.e14)**-0.1
#Above is an example M-c relation. This particular one is complete garbage.

#Results come out in a dictionary
return_dict = Build_Delta_Sigma.build_Delta_Sigma(R,xi_hm,cosmo,input_params)
print return_dict.keys()

R = return_dict["R"]
xi_hm = return_dict['xi_hm']
sigma_r = return_dict['sigma_r']
delta_sigma = return_dict['delta_sigma']
mis_sigma_r = return_dict['miscentered_sigma_r']
mis_delta_sigma = return_dict['miscentered_delta_sigma']

plt.loglog(R,xi_hm,label=r"$\xi_{hm}$")
plt.loglog(R,sigma_r,label=r"$\Sigma$")
plt.loglog(R,delta_sigma,label=r"$\Delta\Sigma$")
plt.loglog(R,mis_sigma_r,c="purple",ls="--",label=r"$\Sigma_{mis}$",alpha=0.8)
plt.loglog(R,mis_delta_sigma,"k--",label=r"$\Delta\Sigma_{mis}$",alpha=0.8)

plt.legend()
plt.xlabel(r"$R\ [Mpc/h]$",fontsize=24)
plt.subplots_adjust(bottom=0.15)
plt.show()
