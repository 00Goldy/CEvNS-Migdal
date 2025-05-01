import matplotlib.pyplot as plt
import numpy as np
import numericalunits as nu

import wimprates as wr
from functions_cevns import dsigma_dER
from functions_cevns import total_flux
from functions_cevns import rate_flamedisx

E_e = np.linspace(1e-1 ,100, 100) #eV
E_v = np.linspace(0.05 ,20, 1000) #MeV
dsigma = []
flux = []
#print(total_flux(0.4))
for Ev in E_v :
    dsigma.append(dsigma_dER(Ev, 0.01))
    flux.append(total_flux(Ev))
#print(wr.get_migdal_transitions_probability_iterators())
"""
plt.figure(figsize=(10, 6))
plt.plot(E_v, dsigma, ":",label='Cross section', color='black')
plt.title(r"CS VS $E_\nu$")
plt.xlabel(r"Neutrino Energy $E_\nu$")
plt.ylabel("Cross section")
#plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
"""

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

Rate = wr.rate_migdal_cevns(
    E_e,
    rate_flamedisx,
    dsigma_dER,
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