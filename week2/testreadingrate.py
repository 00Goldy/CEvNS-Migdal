import pickle
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
import os



def lire_spectre_neutrino(fichier_pkl):
    if not os.path.exists(fichier_pkl):
        raise FileNotFoundError(f"Le fichier '{fichier_pkl}' n'existe pas.")

    # Charger le DataFrame depuis le fichier .pkl
    with open(fichier_pkl, 'rb') as f:
        df = pickle.load(f)

    # Vérifier que c'est bien un DataFrame Pandas
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Le fichier ne contient pas un DataFrame Pandas.")

    # Vérifier les colonnes du DataFrame
    print(f"Colonnes du DataFrame : {df.columns}")

    # Assumer que les colonnes 'energy' et 'flux' existent
    if 'energy(keV)' not in df.columns or 'rate' not in df.columns:
        raise KeyError("Le DataFrame doit contenir les colonnes 'energy' et 'flux'.")

    # Extraire les colonnes energy et flux
    energies = df['energy(keV)']
    flux = df['rate']

    # Affichage du spectre
    print(energies)
    print(flux)

    plt.figure(figsize=(8,5))
    plt.plot(energies, flux, label="Neutrino Spectra")
    plt.xlabel("Recoil Energy (keV)")
    plt.ylabel("Diff Rate (a.u.)")
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Neutrinos spectra via CEvNS")
    plt.legend()
    plt.grid(True)
    plt.show()

    print(trapezoid(flux,energies))

    return energies, flux

# Exemple d'utilisation
if __name__ == "__main__":
    fichier = "CEvNS_solar_total_spectrum.pkl"
    try:
        energies, flux = lire_spectre_neutrino(fichier)
    except Exception as e:
        print(f"Erreur : {e}")