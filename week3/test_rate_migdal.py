import matplotlib.pyplot as plt
import numpy as np
import numericalunits as nu
from scipy.integrate import quad

import wimprates as wr
from functions_cevns import dsigma_dER
from functions_cevns import total_flux
from functions_cevns import rate_flamedisx

E_e = np.linspace(1e-1 ,1e4, 1000) #eV
E_v = np.linspace(0.05 ,20, 1000) #MeV
N_A = 6.022e23
M_Xe = 131.29  # g/mol
N = N_A / (M_Xe * 1e-6) * 3.154e7 #tons-1
dsigma = []
flux = []
#print(total_flux(0.4))
def unit_fun(a,b):
    return 1

def E_nu_min(E_r):
    return 0.5 * (E_r + np.sqrt(E_r**2 + 2 * M_Xe*931.5 * E_r))  # E_r et M en MeV

def Rate(E_v, E_nr):
    return total_flux(E_v) * dsigma_dER(E_v, E_nr)

ENR = np.logspace(np.log10(600),np.log10(6000)) #in eV
r = []
for Er in ENR :
    Er *= 1e-6 #in MeV
    val, _ = quad(lambda E_nu : Rate(E_nu,Er),
                    E_nu_min(Er), #In eV
                    30, #In eV
                    )
    r.append(val*N)

for Ev in E_v :
    flux.append(total_flux(Ev))
    dsigma.append(dsigma_dER(Ev,0.0001))
    

plt.figure(figsize=(10, 6))
plt.plot(ENR, r, ":",label='Diff Rate', color='black')
plt.title(r"dR/dEr VS $E_\nu$")
plt.xlabel(r"NR Energy $E_{NR}$")
plt.ylabel("Differential Rate")
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(E_v, flux, ":",label='Flux', color='black')
plt.title(r"\phi VS $E_\nu$")
plt.xlabel(r"Neutrino Energy $E_\nu$")
plt.ylabel("Flux")
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(E_v, dsigma, ":",label='CS', color='black')
plt.title(r"CS VS $E_\nu$")
plt.xlabel(r"Neutrino Energy $E_\nu$")
plt.ylabel("CS")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

Rate = wr.rate_migdal_cevns(
    E_e,
    rate_flamedisx,
    unit_fun,
)

print(Rate)

"""
plt.plot(E_e, Rate, 'o', label='Migdal Rate', color='black')
plt.title(r"Migdal Rate VS $E_e$")
plt.xlabel(r"Electron Energy $E_e$")
plt.ylabel("Migdal Rate")
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""