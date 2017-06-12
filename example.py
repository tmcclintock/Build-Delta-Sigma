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
import py_Build_Delta_Sigma
import matplotlib.pyplot as plt
import numpy as np

#First load in the halo-matter CF from somewhere
R = np.genfromtxt("test_data/R.txt")
xi_hm = np.genfromtxt("test_data/xi_hm.txt")

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
input_params = {"Mass": 3*10**14.,"delta":200,"timing":1,
                "Rmis":0.25,"fmis":0.25,"miscentering":1}
input_params["concentration"] = 5.0

#Results come out in a dictionary
return_dict = py_Build_Delta_Sigma.build_Delta_Sigma(R,xi_hm,cosmo,input_params)
print return_dict.keys()

R = return_dict["R"]
xi_hm = return_dict['xi_hm']
sigma_r = return_dict['sigma_r']
delta_sigma = return_dict['delta_sigma']
mis_sigma_r = return_dict['miscentered_sigma_r']
mis_delta_sigma = return_dict['miscentered_delta_sigma']
full_delta_sigma = return_dict['full_delta_sigma']

np.savetxt("test_data/delta_sigma_BDS.txt", delta_sigma)

#plt.loglog(R,xi_hm,label=r"$\xi_{hm}$")
#plt.loglog(R,sigma_r,label=r"$\Sigma$")
plt.loglog(R,delta_sigma,label=r"$\Delta\Sigma$",lw=2)
#plt.loglog(R,mis_sigma_r,"--",label=r"$\Sigma_{mis}$",alpha=0.5)
plt.loglog(R,mis_delta_sigma,"--",label=r"$\Delta\Sigma_{mis}$",c='r',lw=2)
#plt.loglog(R,full_delta_sigma,"k-.",label=r"$\Delta\Sigma_{full}$",alpha=0.8,linewidth=2)

plt.legend()
plt.xlabel(r"$R\ [{\rm Mpc}/h]$",fontsize=24)
plt.ylabel(r"$\Delta\Sigma\ [{\rm M_\odot}h/{\rm pc^2}]$",fontsize=24)
plt.subplots_adjust(bottom=0.15)
plt.show()
