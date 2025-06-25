import matplotlib.pyplot as plt

from .datareader import DataReader

def plot_energies(datareader: DataReader):
    """Plots the development of PE, KE, and TE from a DataFrame."""
    # Read energy data
    data = datareader["PE", "KE", "TE"]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(data["PE"], label="Potential Energy (PE)")
    plt.plot(data["KE"], label="Kinetic Energy (KE)")
    plt.plot(data["TE"], label="Total Energy (TE)")
    plt.xlabel("Time step")
    plt.ylabel("Energy")
    plt.title("Energy Development")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()