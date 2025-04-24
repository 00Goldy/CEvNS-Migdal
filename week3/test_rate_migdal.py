import matplotlib.pyplot as plt
import numpy as np
import numericalunits as nu

import wimprates as wr
from functions_cevns import dsigma_dER
from functions_cevns import total_flux

E_e = np.linspace(0.1 ,1e6,10) * nu.keV
E_v = np.linspace(0.1,30, 1000) * nu.MeV

#print(total_flux(0.4))
#print(dsigma_dER(E_v, 0.005))


Rate = wr.rate_migdal_cevns(
    E_e,
    total_flux,
    dsigma_dER,
)

plt.plot(E_e, Rate, ":",label='Migdal Rate', color='black')
plt.title(r"Migdal Rate VS $E_e$")
plt.xlabel(r"Electron Energy $E_e$")
plt.ylabel("Migdal Rate")
#plt.yscale('log')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()