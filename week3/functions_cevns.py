import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
from scipy.interpolate import interp1d

################### CONSTANTS

N = 77
Z = 54
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
    ER_max = (2 * E_v**2) / (m_A + 2 * E_v)
    if E_R > ER_max:
        dsigma.append(0) #There is no CEvNS past ER_max so no cross-section
        print("CPT")
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

#Folder containing data from fluxes
path = "../dataflux"

energy = []
flux = []

# Function to read an concatenate energies and fluxes from sources (contained in path)

def parse_data_block(filepath):
    with open(filepath, 'r') as file:
        data_block = file.read()
    
    lines = data_block.strip().split('\n')
    energies = []
    distrib = []

    for line in lines:
        parts = line.strip().split()
        
        # For 2 columns data file
        if len(parts) == 2:
            try:
                e, phi = map(float, parts)
                energies.append(e)
                distrib.append(phi)
            except ValueError:
                continue

        # For 4 columns data file
        elif len(parts) == 4:
            try:
                e = float(parts[0])
                phi = float(parts[2])
                energies.append(e)
                distrib.append(phi)
            except ValueError:
                continue

        # For 8 columns data file
        elif len(parts) == 8:
            try:
                for i in range(0, 8, 2):
                    e = float(parts[i])
                    phi = float(parts[i+1])
                    energies.append(e)
                    distrib.append(phi)
            except ValueError:
                continue

    return np.array(energies), np.array(distrib)


################### Un-Normalizing 

N7Be = 4.8e9
N8B = 5e6
N13N = 2.9e8
N15O = 2.3e8
N17F = 5.6e6
Npp = 6e10
Nhep = 8e3

####################

interpol_flux = {}

for input_file in os.listdir(path):
    fullpath = os.path.join(path, input_file)
    namesource = input_file.replace(".dat", "")
    print(f"Reading {namesource}...")

    energy, flux = parse_data_block(fullpath)

    if len(energy) == 0:
        print(f"WARNING : {namesource} is empty.")
        continue

    if namesource == '7Be-384' or namesource == '7Be-861':
        if namesource == '7Be-384':
            energy += 384
        else:
            energy += 861
        flux *= N7Be
    
    ## Let's un-normalize fluxes

    if namesource == '8B':
        flux *= N8B
    if namesource == '13N':
        flux *= N13N
    if namesource == '15O':
        flux *= N15O
    if namesource == '17F':
        flux *= N17F
    if namesource == 'pp':
        flux *= Npp
    if namesource == 'hep':
        flux *= Nhep
    
    interp = interp1d(energy, flux, bounds_error = False, fill_value = 0)

    interpol_flux[namesource] = interp

################### Defining function for dflux/dEv

def total_flux(Ev):
    Tot = sum(interp(Ev) for interp in interpol_flux.values())
    return Tot


