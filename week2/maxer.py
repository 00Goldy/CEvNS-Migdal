import matplotlib.pyplot as plt
import numpy as np

E_v = [0.5 , 1,2,5,10,20] #MeV
E_v = np.array(E_v)
E_Rmax = 2*E_v*E_v / (931.5*131.29 + 2*E_v) *1e3

print(E_Rmax)
plt.figure(figsize=(10, 6))
#plt.plot(E_R, dRdERtot/Norm, label='Total Rate',color='blue')  # E_R in keV
plt.plot(E_v, E_Rmax, label='Maximum Er',color='red')
plt.title('Maximum Recoil Energy VS Neutrino Energy')
plt.xscale('log')
plt.xlabel(r"Neutrino energy $E_\nu$ [MeV]")
plt.ylabel(r"Maximum Recoil Energy $E_R^{max}$ [keV]")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.show()