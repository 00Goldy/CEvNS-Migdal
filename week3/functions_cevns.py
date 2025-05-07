import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
from scipy.interpolate import interp1d

################### CONSTANTS

N = 77
Z = 54
G_F = 1.1664e-11 # MeV^-2 Fermi's constant
M_Xe = 131.293 
m_A = M_Xe * 931.5  # MeV/c^2
Q_V = N - 0.1084 * Z
conv = 197.327e-13   # conversion MeV^-1 en cm (from hbar*c = 1)
G_F = conv * 1.1664e-11 # MeV^-2 Fermi's constant in units of hbar*c

# Domain of Ev : from 0.1 to 30 MeV (For testing)
E_v = np.linspace(0.1, 30, 1000)
    
################### Defining function for dsigma/dER

def dsigma_dER(E_v, E_R) :

    dsigma = []
    ER_max = (2 * E_v**2) / (m_A + 2 * E_v)
    #print(ER_max)
    if E_R > ER_max:
        dsigma.append(0) #There is no CEvNS past ER_max so no cross-section
    else:
        val = (G_F**2 * m_A) / (4 * np.pi) * Q_V**2 * (1 - ((m_A * E_R) / (2 * E_v**2)))
        dsigma.append(val)
    dsigma = np.array(dsigma) #convert into an np.array for easy plotting
    #print(dsigma)
    #print('Pipou')
    #print(E_v)
    #print('Pipoudou')
    #print(E_R)
    return dsigma

################### Now for the total solar neutrino flux

# Lire la base de données CSV générée
df = pd.read_csv("../dataflux/total_solar_flux.csv")  # ou mettre le chemin complet si besoin

energy = df["Energy [MeV]"].values
flux = df["Total Flux [cm⁻²·s⁻¹·MeV⁻¹]"].values

# Créer l'interpolation
total_flux_interp = interp1d(energy, flux, bounds_error=False, fill_value=0)

# Fonction d'accès au flux total
def total_flux(Ev):
    return total_flux_interp(Ev)
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

#############################################################
# Flamedisx CEvNS Rate

df = pd.read_pickle("../flamedisxdata/CEvNS_solar_spectrum.pkl")  # ou mettre le chemin complet si besoin

energy = np.array(df["energy_keV"].values)
rate = df["spectrum_value_norm"].values

print(energy)
print(rate)

#energy *= 1e3 #From keV to eV
# Créer l'interpolation
diff_rate_interp = interp1d(energy, rate, bounds_error=False, fill_value=0)

# Fonction d'accès au flux total
def rate_flamedisx(E_nr):
    return diff_rate_interp(E_nr)