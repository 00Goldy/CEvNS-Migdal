import matplotlib.pyplot as plt
import numpy as np
import numericalunits as nu

import wimprates as wr
from functions_cevns import dsigma_dER
from functions_cevns import total_flux

E_e = np.linspace(1 ,70000, 10) #eV
E_v = np.linspace(0.6 ,30, 1000) #MeV
dsigma = []
#print(total_flux(0.4))
for Ev in E_v :
    dsigma.append(dsigma_dER(Ev, 0.01))

#print(wr.get_migdal_transitions_probability_iterators())

plt.plot(E_v, dsigma, ":",label='Cross section', color='black')
plt.title(r"CS VS $E_\nu$")
plt.xlabel(r"Neutrino Energy $E_\nu$")
plt.ylabel("Cross section")
#plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


Rate = wr.rate_migdal_cevns(
    E_e,
    total_flux,
    dsigma_dER,
    E_nu_min = 0.6,
)
print(Rate)
"""
plt.plot(E_e, Rate, ":",label='Migdal Rate', color='black')
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
