import numpy as np
from scipy.integrate import trapezoid

E_v = np.linspace(0.1, 30, 1000)
total_flux = np.ones_like(E_v)
total_fluxB8hep = np.zeros_like(E_v)

Er = 0.5e-3  # 0.5 keV en MeV
m_A = 131
G_F = 1.166e-5
Q_V = 1

Ev_min = np.sqrt(m_A * Er / 2)

mask = E_v >= Ev_min
Ev_valid = E_v[mask]
flux_valid = total_flux[mask]
flux_validB8hep = total_fluxB8hep[mask]

dsigmadEr = ((G_F**2 * m_A) / (4 * np.pi)) * Q_V**2 * (1 - (m_A * Er) / (2 * Ev_valid**2))

integrandtot = flux_valid * dsigmadEr * 3.154e7
integrandB8hep = flux_validB8hep * dsigmadEr * 3.154e7

N = 6.022e23 / (131.29 * 1e-6)
ratetot = N * trapezoid(integrandtot, Ev_valid)
rateB8hep = N * trapezoid(integrandB8hep, Ev_valid)

print("ratetot =", ratetot)
print("rateB8hep =", rateB8hep)
