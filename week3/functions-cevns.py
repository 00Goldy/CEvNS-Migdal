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
m_A = M_Xe * 931.5  # MeV
Q_V = N - 0.1084 * Z
conv = 197.327e-13   # conversion MeV^-1 en cm (from hbar*c = 1)
G_F = conv * 1.1664e-11 # MeV^-2 Fermi's constant in units of hbar*c

# Domain of Ev : from 0.1 to 30 MeV
E_v = np.linspace(0.1, 30, 1000)

################### Defining function for dsigma/dER

def dsigma_dER(E_v, E_R) :

    dsigma = []

    for Ev in E_v:

        ER_max = (2 * Ev**2) / (m_A + 2 * Ev)

        if E_R > ER_max:
            dsigma.append(0) #There is no CEvNS past ER_max so no cross-section

        else:

            val = (G_F**2 * m_A) / (4 * np.pi) * Q_V**2 * (1 - ((m_A * E_R) / (2 * Ev**2)))
            dsigma.append(val)
    dsigma = np.array(dsigma) #convert into an np.array to easy plotting

    return dsigma
#Test
'''
E_v = np.linspace(0.1, 30, 1000)
ER_fixed_values = [0.0001, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02]

plt.figure(figsize=(10, 6))

for i in range(len(ER_fixed_values)):
    dsigma = dsigma_dER(E_v, ER_fixed_values[i])
    plt.plot(E_v, dsigma, label=f"$E_R$ = {ER_fixed_values[i]*1000:.0f} keV")

plt.title(r"Differential Cross Section $\frac{d\sigma}{dE_R}$ vs $E_\nu$")
plt.xlabel("Neutrino Energy $E_\\nu$ [MeV]")
plt.ylabel(r"$\frac{d\sigma}{dE_R}$ [MeV$^{-1}$.cm$^2$]")
plt.xlim(0.1, 30)
plt.legend(title="Fixed $E_R$")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
'''
################### Now for the total solar neutrino flux

path = "../dataflux"

interpol_flux = {}

# Boucle sur tous les fichiers du dossier
for file in os.listdir(path):
    fullpath = os.path.join(path, file)

    namesource = file.replace(".dat", "")

    df = pd.read_csv(fullpath)

    E = df['E'].values
    phi = df['phi'].values

    interp = interp1d(E, phi, bounds_error=False, fill_value=0)

    interpol_flux[namesource] = interp

################### Defining function for dflux/dEv

def total_flux(Ev):
    return sum(interp(Ev) for interp in interpol_flux.values())

plt.figure(figsize=(10, 6))
plt.plot(E_v, total_flux(E_v))
plt.title(r"Differential Cross Section $\frac{d\sigma}{dE_R}$ vs $E_\nu$")
plt.xlabel("Neutrino Energy $E_\\nu$ [MeV]")
plt.ylabel(r"$\frac{d\sigma}{dE_R}$ [MeV$^{-1}$.cm$^2$]")
plt.xlim(0.1, 30)
plt.legend(title="Fixed $E_R$")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()